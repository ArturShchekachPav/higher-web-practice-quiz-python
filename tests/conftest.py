import pytest
from quiz.models import Category, Question, Quiz
from django.urls import reverse

FORM_CATEGORY_DATA = {'title': 'Новое название категории'}

FORM_QUIZ_DATA = {
    'title': 'Новое название квиза',
    'description': 'Новое описание квиза'
}


@pytest.fixture
def category():
    category = Category.objects.create(
        title='Название категории',
    )
    return category


@pytest.fixture
def quiz():
    quiz = Quiz.objects.create(
        title='Название квиза',
        description='Описание квиза'
    )
    return quiz


@pytest.fixture
def question(quiz, category):
    question = Question.objects.create(
        quiz=quiz,
        category=category,
        text='Текст вопроса',
        description='Описание вопроса',
        options=[
            'Правильный ответ',
            'Неправильный ответ'
        ],
        correct_answer='Правильный ответ',
        explanation='Объяснение'
    )
    return question


@pytest.fixture
def quiz_list_create_url():
    return reverse('quiz-list-create')


@pytest.fixture
def quiz_detail_url(quiz):
    return reverse('quiz-detail', args=(quiz.id,))


@pytest.fixture
def quiz_title_url(quiz):
    return reverse('quiz-by-title', args=(quiz.title,))


@pytest.fixture
def quiz_questions(quiz):
    return reverse('quiz-questions', args=(quiz.id,))


@pytest.fixture
def question_list_create_url():
    return reverse('question-list-create')

@pytest.fixture
def question_text_url(question):
    return reverse('question-by-text', args=(question.text,))

@pytest.fixture
def question_detail_url(question):
    return reverse('question-detail', args=(question.id,))


@pytest.fixture
def check_answer_url(question):
    return reverse('question-check', args=(question.id,))


@pytest.fixture
def random_question_url(quiz):
    return reverse('quiz-random-question', args=(quiz.id,))


@pytest.fixture
def category_list_create_url():
    return reverse('category-list-create')


@pytest.fixture
def category_detail_url(category):
    return reverse('category-detail', args=(category.id,))


@pytest.fixture
def form_question_data(category, quiz):
    return {
        'text': 'Новый текст вопроса',
        'category': category.id,
        'quiz': quiz.id,
        'description': 'Новое описание вопроса вопроса',
        'options': [
            'Правильный ответ',
            'Неправильный ответ'
        ],
        'correct_answer': 'Правильный ответ',
        'explanation': 'Новое объявснение'
    }