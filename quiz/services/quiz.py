"""Модуль с реализацией сервиса квизов."""

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuizService
from quiz.models import Quiz
from quiz.utils import update_model_instance


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза."""

    def list_quizzes(self) -> list[Quiz]:
        """Получить список квизов."""
        return list(Quiz.objects.all())

    def get_quiz(self, quiz_id: int) -> Quiz:
        """Получить квиз по идентификатору."""
        return get_object_or_404(Quiz, pk=quiz_id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """Получить список квизов по названию."""
        return list(Quiz.objects.filter(title__icontains=title))

    def create_quiz(self, data: dict) -> Quiz:
        """Создать квиз."""
        return Quiz.objects.create(**data)

    def update_quiz(self, quiz_id: int, data: dict) -> Quiz:
        """Обновить квиз."""
        quiz = self.get_quiz(quiz_id)
        return update_model_instance(quiz, data)

    def delete_quiz(self, quiz_id: int) -> None:
        """Удалить квиз."""
        quiz = self.get_quiz(quiz_id)
        quiz.delete()
