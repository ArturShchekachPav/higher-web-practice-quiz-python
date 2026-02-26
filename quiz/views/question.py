"""Модуль с контроллерами для вопросов."""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService

question_service = QuestionService()
quize_service = QuizService()


class QuestionListCreateView(APIView):
    """Контроллер для получения списка вопросов и создания нового вопроса."""

    def get(self, request: Request) -> Response:
        """Получить список вопросов."""
        questions = question_service.list_questions()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Создать вопрос."""
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz = serializer.validated_data.get('quiz')

        question = question_service.create_question(
            quiz.id, serializer.validated_data
        )

        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_201_CREATED
        )


class QuestionDetailView(APIView):
    """Контроллер для получения, обновления и удаления вопроса по id."""

    def get(self, request: Request, question_id: int) -> Response:
        """Получить вопрос по идентификатору."""
        question = question_service.get_question(question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request: Request, question_id: int) -> Response:
        """Обновить вопрос по идентификатору."""
        question = question_service.get_question(question_id)

        serializer = QuestionSerializer(question, data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_question = question_service.update_question(
            question.id, serializer.validated_data
        )

        return Response(QuestionSerializer(updated_question).data)

    def delete(self, request: Request, question_id: int) -> Request:
        """Удалить вопроса по идентификатору."""
        question_service.delete_question(question_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionsForQuizView(APIView):
    """Контроллер для получения всех вопросов конкретного квиза."""

    def get(self, request: Request, quiz_id: int) -> Response:
        """Получить список вопросов квиза."""
        questions = question_service.get_questions_for_quiz(quiz_id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionsByTextView(APIView):
    """Контроллер для получения вопросов по тексту."""

    def get(self, request: Request, text: str) -> Response:
        """Получить список вопросов по тексту."""
        questions = question_service.get_questions_by_text(text)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class CheckAnswerView(APIView):
    """Контроллер для проверки ответа на вопрос."""

    def post(self, request: Request, question_id: int) -> Response:
        """Проверить правильность ответа."""
        answer = request.data.get('answer')

        if answer is None:
            return Response(
                {'error': 'Ответ не предоставлен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_correct = question_service.check_answer(question_id, answer)
        question = question_service.get_question(question_id)

        return Response({
            'correct': is_correct,
            'correct_answer': (
                question.correct_answer if not is_correct else None
            ),
            'explanation': question.explanation if not is_correct else None
        })


class RandomQuestionFromQuizView(APIView):
    """Контроллер для получения случайного вопроса из квиза."""

    def get(self, request: Request, quiz_id: int) -> Response:
        """Получить случайный вопрос из квиза."""

        question = question_service.random_question_from_quiz(quiz_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
