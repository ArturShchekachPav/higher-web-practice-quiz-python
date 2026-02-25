"""Модуль с контроллерами для вопросов"""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Question, Quiz
from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService

question_service = QuestionService()


class QuestionListCreateView(APIView):
    """Контроллер для получения списка вопросов и создания нового вопроса"""

    def get(self, request: Request) -> Response:
        """Получение списка вопросов"""

        questions = question_service.list_questions()
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Создание вопроса"""

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            quiz = serializer.validated_data.get('quiz')
            if not quiz:
                return Response(
                    {'error': 'quiz обязателен'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            question = question_service.create_question(
                quiz.id, serializer.validated_data
            )
            return Response(
                QuestionSerializer(question).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):
    """Контроллер для получения, обновления и удаления вопроса по id"""

    def get(self, request: Request, question_id: int) -> Response:
        """Получение вопроса по идентификатору"""

        try:
            question = question_service.get_question(question_id)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(
                {'error': 'Вопрос не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request: Request, question_id: int) -> Response:
        """Обновление вопроса по идентификатору"""

        try:
            question = question_service.get_question(question_id)
        except Question.DoesNotExist:
            return Response(
                {'error': 'Вопрос не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuestionSerializer(question, data=request.data)

        if serializer.is_valid():
            updated_question = question_service.update_question(
                question_id, serializer.validated_data
            )
            return Response(QuestionSerializer(updated_question).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, question_id: int) -> Request:
        """Удаление вопроса по идентификатору"""

        try:
            question_service.delete_question(question_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response(
                {'error': 'Вопрос не найден'},
                status=status.HTTP_404_NOT_FOUND
            )


class QuestionsForQuizView(APIView):
    """Контроллер для получения всех вопросов конкретного квиза"""

    def get(self, request: Request, quiz_id: int) -> Response:
        """Получение списка вопросов квиза"""

        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            questions = question_service.get_questions_for_quiz(quiz_id)
            serializer = QuestionSerializer(questions, many=True)
            return Response({
                'quiz': quiz.title,
                'count': len(questions),
                'questions': serializer.data
            })
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'Квиз не найден'},
                status=status.HTTP_404_NOT_FOUND
            )


class QuestionsByTextView(APIView):
    """Контроллер для получения вопросов по тексту"""

    def get(self, request: Request, text: str) -> Response:
        """Получение вопросов по тексту"""

        questions = question_service.get_questions_by_text(text)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class CheckAnswerView(APIView):
    """Контроллер для проверки ответа на вопрос"""

    def post(self, request: Request, question_id: int) -> Response:
        """Проверка правильности ответа"""

        answer = request.data.get('answer')

        if answer is None:
            return Response(
                {'error': 'Ответ не предоставлен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            is_correct = question_service.check_answer(question_id, answer)
            question = question_service.get_question(question_id)

            return Response({
                'correct': is_correct,
                'correct_answer': question.correct_answer if not is_correct else None,
                'explanation': question.explanation if not is_correct else None
            })
        except Question.DoesNotExist:
            return Response(
                {'error': 'Вопрос не найден'},
                status=status.HTTP_404_NOT_FOUND
            )


class RandomQuestionFromQuizView(APIView):
    """Контроллер для получения случайного вопроса из квиза"""

    def get(self, request: Request, quiz_id: int) -> Response:
        """Получение случайного вопроса из квиза по идентификатуру квиза"""

        try:
            question = question_service.random_question_from_quiz(quiz_id)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'Вопросы для данного квиза не найдены'},
                status=status.HTTP_404_NOT_FOUND
            )
