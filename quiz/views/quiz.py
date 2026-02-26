"""Модуль с контроллерами для квизов."""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import QuizSerializer
from quiz.services.quiz import QuizService

quiz_service = QuizService()


class QuizListCreateView(APIView):
    """Контроллер для получения списка квизов и создания нового квиза."""

    def get(self, request: Request) -> Response:
        """Получить список квизов."""
        quizzes = quiz_service.list_quizzes()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Создать квиз."""
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz = quiz_service.create_quiz(serializer.validated_data)

        return Response(
            QuizSerializer(quiz).data, status=status.HTTP_201_CREATED
        )


class QuizDetailView(APIView):
    """Контроллер для получения, обновления и удаления квиза по id."""

    def get(self, request: Request, quiz_id: int) -> Response:
        """Получить квиз по идентификатору."""
        quiz = quiz_service.get_quiz(quiz_id)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def put(self, request: Request, quiz_id: int) -> Response:
        """Обновить квиз по идентификатору."""
        quiz = quiz_service.get_quiz(quiz_id)

        serializer = QuizSerializer(quiz, data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_quiz = quiz_service.update_quiz(
            quiz_id, serializer.validated_data
        )
        return Response(QuizSerializer(updated_quiz).data)

    def delete(self, request: Request, quiz_id: int) -> Response:
        """Удалить квиз."""
        quiz_service.delete_quiz(quiz_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizByTitleView(APIView):
    """Контроллер для получения квизов по названию."""

    def get(self, request: Request, title: str) -> Response:
        """Получить список квизов по названию."""
        quizzes = quiz_service.get_quizes_by_title(title)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
