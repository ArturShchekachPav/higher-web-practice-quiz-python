import pytest
from rest_framework import status

from tests.conftest import FORM_CATEGORY_DATA, FORM_QUIZ_DATA

pytestmark = pytest.mark.django_db


class TestCategoryAPI:
    def test_create_category(self, client, category_list_create_url):
        """Тест создания категории."""
        response = client.post(
            category_list_create_url,
            FORM_CATEGORY_DATA,
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_201_CREATED

        category_data = response.json()

        assert category_data['title'] == FORM_CATEGORY_DATA['title']

    def test_get_categories_list(
        self, client, category_list_create_url, category
    ):
        """Тест получения списка категорий."""
        response = client.get(category_list_create_url)

        assert response.status_code == status.HTTP_200_OK

        categories_data = response.json()

        assert isinstance(categories_data, list)
        assert categories_data

        category_data = categories_data[0]

        assert category_data['title'] == category.title

    def test_get_category(self, client, category_detail_url, category):
        """Тест получения категории."""
        response = client.get(category_detail_url)

        assert response.status_code == status.HTTP_200_OK

        category_data = response.json()

        assert category_data['title'] == category.title

    def test_update_category(self, client, category_detail_url):
        """Тест обновления категории."""
        response = client.put(
            category_detail_url,
            FORM_CATEGORY_DATA,
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_200_OK

        updated_category_data = response.json()

        assert updated_category_data['title'] == FORM_CATEGORY_DATA['title']

    def test_delete_category(self, client, category_detail_url):
        """Тест удаления категории."""
        response = client.delete(category_detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_category_empty_title(
        self, client, category_list_create_url
    ):
        """Тест создания категории с пустым названием."""
        response = client.post(
            category_list_create_url,
            {'title': ''},
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestQuizAPI:
    def test_create_quiz(self, client, quiz_list_create_url):
        """Тест создания квиза."""
        response = client.post(
            quiz_list_create_url,
            FORM_QUIZ_DATA,
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_201_CREATED

        quiz_data = response.json()

        assert quiz_data['title'] == FORM_QUIZ_DATA['title']
        assert quiz_data['description'] == FORM_QUIZ_DATA['description']

    def test_get_quizzes_list(
        self, client, quiz_list_create_url, quiz
    ):
        """Тест получения списка квизов."""
        response = client.get(quiz_list_create_url)

        assert response.status_code == status.HTTP_200_OK

        quizzes_data = response.json()

        assert isinstance(quizzes_data, list)
        assert quizzes_data

        quiz_data = quizzes_data[0]

        assert quiz_data['title'] == quiz.title
        assert quiz_data['description'] == quiz.description

    def test_get_quizzes_by_title(
        self, client, quiz_title_url, quiz
    ):
        """Тест получения списка квизов по заголовку."""
        response = client.get(quiz_title_url)

        assert response.status_code == status.HTTP_200_OK

        quizzes_data = response.json()

        assert isinstance(quizzes_data, list)
        assert quizzes_data

        quiz_data = quizzes_data[0]

        assert quiz_data['title'] == quiz.title
        assert quiz_data['description'] == quiz.description

    def test_get_quiz(self, client, quiz_detail_url, quiz):
        """Тест получения квиза."""
        response = client.get(quiz_detail_url)

        assert response.status_code == status.HTTP_200_OK

        quiz_data = response.json()

        assert quiz_data['title'] == quiz.title
        assert quiz_data['description'] == quiz.description

    def test_update_quiz(self, client, quiz_detail_url):
        """Тест обновления квиза."""
        response = client.put(
            quiz_detail_url,
            FORM_QUIZ_DATA,
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_200_OK

        updated_quiz_data = response.json()

        assert updated_quiz_data['title'] == FORM_QUIZ_DATA['title']
        assert (updated_quiz_data['description']
                == FORM_QUIZ_DATA['description'])

    def test_delete_quiz(self, client, quiz_detail_url):
        """Тест удаления квиза."""
        response = client.delete(quiz_detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestQuestionAPI:
    def test_create_question(
        self, client, question_list_create_url, form_question_data
    ):
        """Тест создания вопроса."""
        response = client.post(
            question_list_create_url,
            form_question_data,
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_201_CREATED

        question_data = response.json()

        assert form_question_data['text'] == question_data['text']
        assert (form_question_data['description']
                == question_data['description'])
        assert form_question_data['options'] == question_data['options']
        assert (form_question_data['correct_answer']
                == question_data['correct_answer'])
        assert (form_question_data['explanation']
                == question_data['explanation'])

    def test_get_questions_list(
        self, client, question_list_create_url, question
    ):
        """Тест получения списка вопросов."""
        response = client.get(question_list_create_url)

        assert response.status_code == status.HTTP_200_OK

        questions_data = response.json()

        assert isinstance(questions_data, list)
        assert questions_data

        question_data = questions_data[0]

        assert question.text == question_data['text']
        assert question.description == question_data['description']
        assert question.options == question_data['options']
        assert question.correct_answer == question_data['correct_answer']
        assert question.explanation == question_data['explanation']

    def test_get_questions_by_text(
        self, client, question_text_url, question
    ):
        """Тест получения списка вопросов по тексту."""
        response = client.get(question_text_url)

        assert response.status_code == status.HTTP_200_OK

        questions_data = response.json()

        assert isinstance(questions_data, list)
        assert questions_data

        question_data = questions_data[0]

        assert question.text == question_data['text']
        assert question.description == question_data['description']
        assert question.options == question_data['options']
        assert question.correct_answer == question_data['correct_answer']
        assert question.explanation == question_data['explanation']

    def test_get_question(self, client, question_detail_url, question):
        """Тест получения вопроса."""
        response = client.get(question_detail_url)

        assert response.status_code == status.HTTP_200_OK

        question_data = response.json()

        assert question.text == question_data['text']
        assert question.description == question_data['description']
        assert question.options == question_data['options']
        assert question.correct_answer == question_data['correct_answer']
        assert question.explanation == question_data['explanation']

    def test_update_question(
        self, client, question_detail_url, form_question_data
    ):
        """Тест обновления вопроса."""
        response = client.put(
            question_detail_url,
            form_question_data,
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_200_OK

        updated_question_data = response.json()

        assert form_question_data['text'] == updated_question_data['text']
        assert (form_question_data['description']
                == updated_question_data['description'])
        assert (form_question_data['options']
                == updated_question_data['options'])
        assert (form_question_data['correct_answer']
                == updated_question_data['correct_answer'])
        assert (form_question_data['explanation']
                == updated_question_data['explanation'])

    def test_delete_question(self, client, question_detail_url):
        """Тест удаления вопроса."""
        response = client.delete(question_detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_check_answer(self, client, check_answer_url, question):
        """Тест проверки ответа."""
        response = client.post(
            check_answer_url,
            {
                'answer': question.correct_answer
            },
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data['correct'] is True

    def test_get_random_question(self, client, random_question_url, question):
        """Тест получения случайного вопроса."""
        response = client.get(random_question_url)

        assert response.status_code == status.HTTP_200_OK

        question_data = response.json()

        assert question.text == question_data['text']
        assert question.description == question_data['description']
        assert question.options == question_data['options']
        assert question.correct_answer == question_data['correct_answer']
        assert question.explanation == question_data['explanation']

    def test_create_question_missing_quiz(
        self, client, question_list_create_url, form_question_data
    ):
        """Тест создания вопроса без quiz."""
        data = form_question_data.copy()

        del data['quiz']

        response = client.post(
            question_list_create_url,
            data,
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_check_answer_wrong(self, client, check_answer_url, question):
        """Тест проверки неправильного ответа."""
        response = client.post(
            check_answer_url,
            {'answer': 'Неправильный ответ'},
            content_type='application/json'
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['correct'] is False
        assert 'correct_answer' in data
        assert 'explanation' in data

    def test_check_answer_missing_answer(self, client, check_answer_url):
        """Тест проверки без поля answer."""
        response = client.post(
            check_answer_url,
            {},
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
