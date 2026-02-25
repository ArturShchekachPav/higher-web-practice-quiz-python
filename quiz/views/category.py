"""Модуль с контроллерами для категорий"""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Category
from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService

category_service = CategoryService()


class CategoryListCreateView(APIView):
    """Контроллер для получения списка категорий и создания новой категории"""

    def get(self, request: Request) -> Response:
        """Получение списка категорий"""

        categories = category_service.list_categories()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Создание категории"""

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            category = category_service.create_category(
                **serializer.validated_data
            )
            return Response(
                CategorySerializer(category).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    """Контроллер для получения, обновления и удаления категории по id"""

    def get(self, request: Request, category_id: int) -> Response:
        """Получение вопроса по идентификатору"""

        try:
            category = category_service.get_category(category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(
                {'error': 'Категория не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request: Request, category_id: int) -> Response:
        """Обновление категории по идентификатору"""

        try:
            category = category_service.get_category(category_id)
        except Category.DoesNotExist:
            return Response(
                {'error': 'Категория не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            updated_category = category_service.update_category(
                category_id,
                serializer.validated_data
            )
            return Response(CategorySerializer(updated_category).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, category_id: int) -> Response:
        """Удаление категории по идентификатору"""

        try:
            category_service.delete_category(category_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(
                {'error': 'Категория не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
