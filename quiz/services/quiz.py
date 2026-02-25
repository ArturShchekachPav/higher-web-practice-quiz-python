"""Модуль с реализацией сервиса квизов"""


from quiz.dao import AbstractQuizService
from quiz.models import Quiz


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза"""

    def list_quizzes(self) -> list[Quiz]:
        """Получение списка квизов"""

        return list(Quiz.objects.all())

    def get_quiz(self, id: int) -> Quiz:
        """Получение квиза по id"""

        return Quiz.objects.get(pk=id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """Получение квизов по названию"""

        return list(Quiz.objects.filter(title__icontains=title))

    def create_quiz(self, data: dict) -> Quiz:
        """Создание квиза"""

        return Quiz.objects.create(**data)

    def update_quiz(self, id: int, data: dict) -> Quiz:
        """Обновление квиза по id"""

        quiz = self.get_quiz(id)

        for key, value in data.items():
            setattr(quiz, key, value)

        quiz.save()
        return quiz

    def delete_quiz(self, id: int) -> None:
        """Удаление квиза по id"""

        Quiz.objects.get(pk=id).delete()
