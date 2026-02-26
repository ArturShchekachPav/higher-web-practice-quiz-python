"""Модуль с контроллерами для категорий."""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService

category_service = CategoryService()


class CategoryListCreateView(APIView):
    """Контроллер для получения списка категорий и создания новой категории."""

    def get(self, request: Request) -> Response:
        """Получить список категорий."""
        categories = category_service.list_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Создать категорию."""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = category_service.create_category(
            **serializer.validated_data
        )

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )


class CategoryDetailView(APIView):
    """Контроллер для получения, обновления и удаления категории по id"""

    def get(self, request: Request, category_id: int) -> Response:
        """Получить вопрос по идентификатору."""
        category = category_service.get_category(category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request: Request, category_id: int) -> Response:
        """Обновить категорию"""
        category = category_service.get_category(category_id)

        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_category = category_service.update_category(
            category.id,
            serializer.validated_data
        )

        return Response(CategorySerializer(updated_category).data)

    def delete(self, request: Request, category_id: int) -> Response:
        """Удалить категорию по идентификатору"""
        category_service.delete_category(category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
