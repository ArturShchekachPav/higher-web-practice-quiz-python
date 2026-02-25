import pytest
from quiz.models import Category, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.quiz import QuizService
from quiz.services.question import QuestionService
from tests.conftest import (
    FORM_CATEGORY_DATA, FORM_QUIZ_DATA
)

pytestmark = pytest.mark.django_db


class TestCategoryService:
    def setup_method(self) -> None:
        """Подготавливает сервис"""

        self.service = CategoryService()

    def test_create_category(self) -> None:
        """Тест создания категории"""

        initial_categories_count = Category.objects.count()

        category = self.service.create_category(FORM_CATEGORY_DATA['title'])

        final_categories_count = Category.objects.count()

        assert final_categories_count == initial_categories_count + 1
        assert isinstance(category, Category)
        assert category.title == FORM_CATEGORY_DATA['title']

    def test_get_categories_list(self, category) -> None:
        """Тест получения списка категорий"""

        categories = self.service.list_categories()

        assert categories == [category]

    def test_get_category(self, category) -> None:
        """Тест получения категории"""

        resulting_category = self.service.get_category(category.id)

        assert resulting_category == category

    def test_update_category(self, category) -> None:
        """Тест обновления категории"""

        initial_categories_count = Category.objects.count()

        updated_category = self.service.update_category(
            category.id, FORM_CATEGORY_DATA
        )

        final_categories_count = Category.objects.count()

        assert final_categories_count == initial_categories_count
        assert isinstance(updated_category, Category)
        assert updated_category.title == FORM_CATEGORY_DATA['title']

    def test_delete_category(self, category) -> None:
        """Тест удаления категории"""

        initial_categories_count = Category.objects.count()

        self.service.delete_category(category.id)

        final_categories_count = Category.objects.count()

        assert initial_categories_count - 1 == final_categories_count

    def test_get_category_not_found(self) -> None:
        """Тест получения несуществующей категории"""

        with pytest.raises(Category.DoesNotExist):
            self.service.get_category(999)

    def test_update_category_not_found(self) -> None:
        """Тест обновления несуществующей категории"""

        with pytest.raises(Category.DoesNotExist):
            self.service.update_category(999, FORM_CATEGORY_DATA)

    def test_delete_category_not_found(self) -> None:
        """Тест удаления несуществующей категории"""

        with pytest.raises(Category.DoesNotExist):
            self.service.delete_category(999)

    def test_create_category_empty_title(self) -> None:
        """Тест создания категории с пустым названием"""

        with pytest.raises(Exception):
            self.service.create_category('')


class TestQuizService:
    def setup_method(self) -> None:
        """Подготавливает сервис"""

        self.service = QuizService()

    def test_create_quiz(self) -> None:
        """Тест создания квиза"""

        initial_quizzes_count = Quiz.objects.count()

        quiz = self.service.create_quiz(FORM_QUIZ_DATA)

        final_quizzes_count = Quiz.objects.count()

        assert final_quizzes_count == initial_quizzes_count + 1
        assert isinstance(quiz, Quiz)
        assert quiz.title == FORM_QUIZ_DATA['title']
        assert quiz.description == FORM_QUIZ_DATA['description']

    def test_get_quizzes_list(self, quiz) -> None:
        """Тест получения списка квизов"""

        quizzes = self.service.list_quizzes()

        assert quizzes == [quiz]

    def test_get_quiz_by_id(self, quiz) -> None:
        """Тест получения квиза по id"""

        resulting_quiz = self.service.get_quiz(quiz.id)

        assert resulting_quiz == quiz

    def test_get_quiz_by_title(self, quiz) -> None:
        """Тест получения квиза по title"""

        quizzes = self.service.get_quizes_by_title(quiz.title)

        assert quizzes == [quiz]

    def test_update_quiz(self, quiz) -> None:
        """Тест обновления квиза"""

        initial_quizzes_count = Quiz.objects.count()

        updated_quiz = self.service.update_quiz(
            quiz.id, FORM_QUIZ_DATA
        )

        final_quizzes_count = Quiz.objects.count()

        assert final_quizzes_count == initial_quizzes_count
        assert isinstance(updated_quiz, Quiz)
        assert updated_quiz.title == FORM_QUIZ_DATA['title']
        assert updated_quiz.description == FORM_QUIZ_DATA['description']

    def test_delete_quiz(self, quiz) -> None:
        """Тест удаления квиза"""

        initial_quizzes_count = Quiz.objects.count()

        self.service.delete_quiz(quiz.id)

        final_quizzes_count = Quiz.objects.count()

        assert initial_quizzes_count - 1 == final_quizzes_count

    def test_get_quiz_not_found(self) -> None:
        """Тест получения несуществующего квиза"""

        with pytest.raises(Quiz.DoesNotExist):
            self.service.get_quiz(999)

    def test_update_quiz_not_found(self) -> None:
        """Тест обновления несуществующего квиза"""

        with pytest.raises(Quiz.DoesNotExist):
            self.service.update_quiz(999, FORM_QUIZ_DATA)

    def test_delete_quiz_not_found(self) -> None:
        """Тест удаления несуществующего квиза"""

        with pytest.raises(Quiz.DoesNotExist):
            self.service.delete_quiz(999)

    def test_get_quizes_by_title_empty(self) -> None:
        """Тест поиска квизов по пустому названию"""

        quizzes = self.service.get_quizes_by_title('')
        assert isinstance(quizzes, list)

    def test_get_quizes_by_title_no_results(self, quiz) -> None:
        """Тест поиска квизов по несуществующему названию"""
        quizzes = self.service.get_quizes_by_title('NonExistentTitle')
        assert quizzes == []


class TestQuestionService:
    def setup_method(self) -> None:
        """Подготавливает сервис"""

        self.service = QuestionService()

    def test_create_question(self, quiz, category, form_question_data) -> None:
        """Тест создания вопроса"""

        initial_questions_count = Question.objects.count()

        question_data = form_question_data.copy()
        question_data['category'] = category
        question_data['quiz'] = quiz

        question = self.service.create_question(quiz.id, question_data)

        final_questions_count = Question.objects.count()

        assert final_questions_count == initial_questions_count + 1
        assert isinstance(question, Question)
        assert question.text == question_data['text']
        assert question.description == question_data['description']
        assert question.options == question_data['options']
        assert question.correct_answer == question_data['correct_answer']
        assert question.explanation == question_data['explanation']

    def test_get_questions_list(self, question) -> None:
        """Тест получения списка вопросов"""

        questions = self.service.list_questions()

        assert questions == [question]

    def test_get_question_by_id(self, question) -> None:
        """Тест получения вопроса по id"""

        resulting_question = self.service.get_question(question.id)

        assert resulting_question == question

    def test_get_question_by_text(self, question) -> None:
        """Тест получения вопроса по text"""

        questions = self.service.get_questions_by_text(question.text)

        assert questions == [question]

    def test_update_question(
        self, question, category, quiz, form_question_data
    ):
        """Тест обновления вопроса"""

        initial_questions_count = Question.objects.count()

        question_data = form_question_data.copy()
        question_data['category'] = category
        question_data['quiz'] = quiz

        updated_question = self.service.update_question(
            question.id, question_data
        )

        final_questions_count = Question.objects.count()

        assert final_questions_count == initial_questions_count
        assert isinstance(updated_question, Question)
        assert updated_question.text == question_data['text']
        assert (updated_question.description
                == question_data['description'])
        assert updated_question.options == question_data['options']
        assert (updated_question.correct_answer
                == question_data['correct_answer'])
        assert (updated_question.explanation
                == question_data['explanation'])

    def test_delete_question(self, question) -> None:
        """Тест удаления вопроса"""

        initial_questions_count = Question.objects.count()

        self.service.delete_question(question.id)

        final_questions_count = Question.objects.count()

        assert initial_questions_count - 1 == final_questions_count

    def test_get_quiz_questions(self, question, quiz) -> None:
        """Тест получения вопросов квиза"""

        questions = self.service.get_questions_for_quiz(quiz.id)

        assert questions == [question]

    def test_check_answer(self, question) -> None:
        """Тест проверки правильности ответа"""

        right_answer = self.service.check_answer(
            question.id, question.correct_answer
        )
        wrong_answer = self.service.check_answer(
            question.id, 'Неправильный ответ'
        )

        assert right_answer
        assert not wrong_answer

    def test_get_random_question(self, question, quiz) -> None:
        """Тест получения случайного вопроса"""

        resulting_question = self.service.random_question_from_quiz(quiz.id)

        assert resulting_question == question

    def test_create_question_missing_required_fields(self, quiz) -> None:
        """Тест создания вопроса без обязательных полей"""

        incomplete_data = {'text': 'Текст вопроса'}

        with pytest.raises(Exception):
            self.service.create_question(quiz.id, incomplete_data)

    def test_create_question_invalid_options(self, quiz) -> None:
        """Тест создания вопроса с невалидными options"""

        invalid_data = {
            'text': 'Вопрос',
            'options': ['только один'],
            'correct_answer': 'только один',
            'difficulty': 'easy'
        }
        with pytest.raises(Exception):
            self.service.create_question(quiz.id, invalid_data)

    def test_create_question_wrong_answer_not_in_options(self, quiz) -> None:
        """Тест создания вопроса с ответом не из options"""

        invalid_data = {
            'text': 'Вопрос',
            'options': ['A', 'B'],
            'correct_answer': 'C',
            'difficulty': 'easy'
        }

        with pytest.raises(Exception):
            self.service.create_question(quiz.id, invalid_data)

    def test_get_question_not_found(self) -> None:
        """Тест получения несуществующего вопроса"""

        with pytest.raises(Question.DoesNotExist):
            self.service.get_question(999)

    def test_update_question_not_found(self, form_question_data) -> None:
        """Тест обновления несуществующего вопроса"""

        with pytest.raises(Question.DoesNotExist):
            self.service.update_question(999, form_question_data)

    def test_delete_question_not_found(self) -> None:
        """Тест удаления несуществующего вопроса"""

        with pytest.raises(Question.DoesNotExist):
            self.service.delete_question(999)

    def test_get_questions_for_quiz_empty(self, quiz) -> None:
        """Тест получения вопросов для квиза без вопросов"""

        questions = self.service.get_questions_for_quiz(quiz.id)

        assert questions == []

    def test_check_answer_empty_string(self, question) -> None:
        """Тест проверки ответа с пустой строкой"""

        result = self.service.check_answer(question.id, '')

        assert result is False

    def test_check_answer_case_sensitive(self, question) -> None:
        """Тест проверки регистрозависимости ответа"""

        result = self.service.check_answer(
            question.id, 
            question.correct_answer.lower()
        )

        assert result is False

    def test_check_answer_with_spaces(self, question) -> None:
        """Тест проверки ответа с лишними пробелами"""

        result = self.service.check_answer(
            question.id,
            f'  {question.correct_answer}  '
        )

        assert result is False

    def test_random_question_from_empty_quiz(self, quiz) -> None:
        """Тест получения случайного вопроса из пустого квиза"""

        with pytest.raises(Quiz.DoesNotExist):
            self.service.random_question_from_quiz(quiz.id)

    def test_random_question_from_nonexistent_quiz(self) -> None:
        """Тест получения случайного вопроса из несуществующего квиза"""

        with pytest.raises(Quiz.DoesNotExist):
            self.service.random_question_from_quiz(999)
