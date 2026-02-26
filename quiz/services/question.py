"""Модуль с реализацией сервиса вопросов."""

import random

from django.http import Http404
from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuestionService
from quiz.models import Question
from quiz.services.quiz import QuizService
from quiz.utils import update_model_instance

quiz_service = QuizService()


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов."""

    def list_questions(self) -> list[Question]:
        """Получить список вопросов."""
        return list(Question.objects.all())

    def get_question(self, question_id: int) -> Question:
        """Получить вопрос по индектификатору."""
        return get_object_or_404(Question, pk=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        """Получить вопросы по тексту."""
        return list(Question.objects.filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        """Получить все вопросы квиза по индентификатору."""
        quiz = quiz_service.get_quiz(quiz_id)
        return list(Question.objects.filter(quiz_id=quiz.id))

    def create_question(self, quiz_id: int, data: dict) -> Question:
        """Создать вопрос."""
        return Question.objects.create(quiz_id=quiz_id, **data)

    def update_question(self, question_id: int, data: dict) -> Question:
        """Обновить вопрос."""
        question = self.get_question(question_id)
        return update_model_instance(question, data)

    def delete_question(self, question_id: int) -> None:
        """Удалить вопрос."""
        question = self.get_question(question_id)
        question.delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        """Проверить корректность ответа на вопрос."""
        question = self.get_question(question_id)
        return question.correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        """Получить случайный вопроса из квиза."""
        quiz = quiz_service.get_quiz(quiz_id)

        questions = self.get_questions_for_quiz(quiz.id)

        if not questions:
            raise Http404(f'No questions found for quiz {quiz_id}')

        return random.choice(questions)
