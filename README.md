# API для QUIZ

## Описание
Проект представляет собой API для сервиса квизов. API позволяет получать, создавать и редактировать категории, квизы и вопросы.

## Стек
Python/Django/DRF

## Установка
```bash
uv sync
source .venv/Scripts/Activate
python manage.py migrate
python manage.py runserver
```

Документация: http://127.0.0.1:8000/redoc

## Примеры запросов
```bash
URL: http://127.0.0.1:8000/api/category/
Method: GET
Responce: [
    {
        "id": 1,
        "title": "jkflds название категории"
    }
]

URL: http://127.0.0.1:8000/api/question/
Method: GET
Responce: [
    {
        "id": 1,
        "text": "Новый текст вопроса",
        "description": "Новое описание вопроса вопроса",
        "options": [
            "Правильный ответ",
            "Неправильный ответ"
        ],
        "correct_answer": "Правильный ответ",
        "explanation": "Новое объявснение",
        "difficulty": "medium",
        "quiz": 1,
        "category": 1
    }
]
```

## Автор
Щекач Артур - fullstack developer