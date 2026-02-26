"""Модуль с реализацией сервиса категорий."""

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractCategoryService
from quiz.models import Category
from quiz.utils import update_model_instance


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий"""

    def list_categories(self) -> list[Category]:
        """Получить список категорий."""
        return list(Category.objects.all())

    def get_category(self, category_id: int) -> Category:
        """Получить категорию по идентификатору."""
        return get_object_or_404(Category, pk=category_id)

    def create_category(self, title: str) -> Category:
        """Создать категорию или вернуть существующую."""
        category, _ = Category.objects.get_or_create(title=title)
        return category

    def update_category(self, category_id: int, data: dict) -> Category:
        """Обновить категорию"""
        category = self.get_category(category_id)
        return update_model_instance(category, data)

    def delete_category(self, category_id: int) -> None:
        """Удалить категорию."""
        category = self.get_category(category_id)
        category.delete()
