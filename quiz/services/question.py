"""Модуль с реализацией сервиса вопросов"""

import random

from quiz.dao import AbstractQuestionService
from quiz.models import Question, Quiz


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов"""

    def list_questions(self) -> list[Question]:
        """Получение списка вопросов"""

        return list(Question.objects.all())

    def get_question(self, question_id: int) -> Question:
        """Получение вопроса"""

        return Question.objects.get(pk=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        """Получить вопросы по тексту"""

        return list(Question.objects.filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        """Получение всех вопросов квиза"""

        return list(Question.objects.filter(quiz_id=quiz_id))

    def create_question(self, quiz_id: int, data: dict) -> Question:
        """Создание вопроса"""

        return Question.objects.create(quiz_id=quiz_id, **data)

    def update_question(self, question_id: int, data: dict) -> Question:
        """Обновление вопроса"""

        question = self.get_question(question_id)

        for key, value in data.items():
            setattr(question, key, value)

        question.save()
        return question

    def delete_question(self, question_id: int) -> None:
        """Удаление вопроса"""

        Question.objects.get(pk=question_id).delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        """Проверка корректности ответа на вопрос"""

        question = self.get_question(question_id)
        return question.correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        """Получение случайного вопроса из квиза"""

        questions = list(Question.objects.filter(quiz_id=quiz_id))

        if not questions:
            raise Quiz.DoesNotExist(f'No questions found for quiz {quiz_id}')

        return random.choice(questions)
