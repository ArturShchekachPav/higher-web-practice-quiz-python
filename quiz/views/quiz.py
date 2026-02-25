"""Модуль с контроллерами для квизов"""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Quiz
from quiz.serializers import QuizSerializer
from quiz.services.quiz import QuizService

quiz_service = QuizService()


class QuizListCreateView(APIView):
    """Контроллер для получения списка квизов и создания нового квиза"""

    def get(self, request: Request) -> Response:
        """Получение квизов"""

        quizzes = quiz_service.list_quizzes()
        serializer = QuizSerializer(quizzes, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Создание квиза"""

        serializer = QuizSerializer(data=request.data)

        if serializer.is_valid():
            quiz = quiz_service.create_quiz(serializer.validated_data)
            return Response(
                QuizSerializer(quiz).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetailView(APIView):
    """Контроллер для получения, обновления и удаления квиза по id"""

    def get(self, request: Request, quiz_id: int) -> Response:
        """Получение квиза по идентификатору"""

        try:
            quiz = quiz_service.get_quiz(quiz_id)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'Квиз не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request: Request, quiz_id: int) -> Response:
        """Обновление квиза по идентификатору"""

        try:
            quiz = quiz_service.get_quiz(quiz_id)
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'Квиз не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuizSerializer(quiz, data=request.data)

        if serializer.is_valid():
            updated_quiz = quiz_service.update_quiz(
                quiz_id, serializer.validated_data
            )
            return Response(QuizSerializer(updated_quiz).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, quiz_id: int) -> Response:
        """Удаление квиза по идентификатору"""

        try:
            quiz_service.delete_quiz(quiz_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'Квиз не найден'},
                status=status.HTTP_404_NOT_FOUND
            )


class QuizByTitleView(APIView):
    """Контроллер для получения квизов по названию"""

    def get(self, request: Request, title: str) -> Response:
        """Получение квизов по названию"""
        quizzes = quiz_service.get_quizes_by_title(title)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
