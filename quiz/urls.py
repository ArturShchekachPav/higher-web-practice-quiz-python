"""Модуль c роутингом"""

from django.urls import include, path

from quiz.views.category import CategoryDetailView, CategoryListCreateView
from quiz.views.question import (
    CheckAnswerView,
    QuestionDetailView,
    QuestionListCreateView,
    QuestionsByTextView,
    QuestionsForQuizView,
    RandomQuestionFromQuizView,
)
from quiz.views.quiz import QuizByTitleView, QuizDetailView, QuizListCreateView

questions_urls = [
    path(
        '',
        QuestionListCreateView.as_view(),
        name='question-list-create'
    ),
    path(
        '<int:question_id>',
        QuestionDetailView.as_view(),
        name='question-detail'
    ),
    path(
        'by_text/<str:text>',
        QuestionsByTextView.as_view(),
        name='question-by-text'
    ),
    path(
        '<int:question_id>/check',
        CheckAnswerView.as_view(),
        name='question-check'
    ),
]

quizes_urls = [
    path('', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
    path(
        'by_title/<str:title>/',
        QuizByTitleView.as_view(),
        name='quiz-by-title'
    ),
    path(
        '<int:quiz_id>/random_question/',
        RandomQuestionFromQuizView.as_view(),
        name='quiz-random-question'
    ),
    path(
        '<int:quiz_id>/questions',
        QuestionsForQuizView.as_view(),
        name='quiz-questions'
    ),
]

categories_urls = [
    path('', CategoryListCreateView.as_view(), name='category-list-create'),
    path(
        '<int:category_id>/',
        CategoryDetailView.as_view(),
        name='category-detail'
    ),
]

urlpatterns = [
    path('question/', include(questions_urls)),
    path('quiz/', include(quizes_urls)),
    path('category/', include(categories_urls)),
]
