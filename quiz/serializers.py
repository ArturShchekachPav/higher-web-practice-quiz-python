"""Модуль c сериализаторами"""

from rest_framework import serializers

from quiz.models import Category, Question, Quiz


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        """Мета-класс для настройки сериализатора."""

        model = Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов."""

    class Meta:
        """Мета-класс для настройки сериализатора."""

        model = Question
        fields = '__all__'

    def validate(self, data: dict[str, any]) -> dict[str, any]:
        """Метод для валидации сериализатора."""
        options = data.get('options')
        correct_answer = data.get('correct_answer')

        if options and correct_answer and correct_answer not in options:
            raise serializers.ValidationError({
                'correct_answer': f'"{correct_answer}" нет в вариантах ответов'
            })

        return data


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для квизов."""

    class Meta:
        """Мета-класс для настройки сериализатора."""

        model = Quiz
        fields = '__all__'
