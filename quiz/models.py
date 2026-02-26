"""Модуль c моделями приложения quiz"""

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import Truncator

from quiz.constants import (
    CATEGORY_TITLE_MAX_LEN,
    CATEGORY_TITLE_MIN_LEN,
    CORRECT_ANSWER_MAX_LEN,
    EXPALANATION_MAX_LEN,
    MIN_OPTIONS_CHOICES_COUNT,
    QUIZ_TITLE_MAX_LEN,
    SHORT_STR_LEN,
    TEXT_FIELD_MAX_LEN,
)
from quiz.validators import validate_options


class Category(models.Model):
    """Модель категории вопросов."""

    title = models.CharField(
        'Название',
        max_length=CATEGORY_TITLE_MAX_LEN,
        validators=[
            MinLengthValidator(
                CATEGORY_TITLE_MIN_LEN,
                message='Название не может быть пустым'
            )
        ]
    )

    class Meta:
        """Мета-класс для категории."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self) -> str:
        """Строковое представление категории."""
        return Truncator(self.title).chars(SHORT_STR_LEN)


class Quiz(models.Model):
    """Модель квиза."""

    title = models.CharField('Название', max_length=QUIZ_TITLE_MAX_LEN)
    description = models.TextField(
        'Описание',
        max_length=TEXT_FIELD_MAX_LEN,
        blank=True
    )

    class Meta:
        """Мета-класс для квиза."""

        verbose_name = 'Квиз'
        verbose_name_plural = 'Квизы'
        ordering = ['title']

    def __str__(self) -> str:
        """Строковое представление квиза."""
        return Truncator(self.title).chars(SHORT_STR_LEN)


class Difficulty(models.TextChoices):
    """Варианты сложностей для вопросов."""

    EASY = 'easy', 'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'

    @classmethod
    def max_length(cls) -> int:
        """Вернуть максимальную длину значения."""
        return max(len(value) for value, _ in cls.choices)


class Question(models.Model):
    """Модель вопроса."""

    quiz = models.ForeignKey(
        Quiz,
        verbose_name='Квиз',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='questions'
    )
    text = models.TextField(
        'Текст',
        max_length=TEXT_FIELD_MAX_LEN
    )
    description = models.TextField(
        'Описание',
        max_length=TEXT_FIELD_MAX_LEN,
        blank=True
    )
    options = models.JSONField(
        'Варианты ответов',
        validators=[validate_options],
        help_text=(
            'Массив строк с вариантами ответов, '
            f'минимум {MIN_OPTIONS_CHOICES_COUNT} варианта'
        )
    )
    correct_answer = models.CharField(
        'Правильный ответ',
        max_length=CORRECT_ANSWER_MAX_LEN
    )
    explanation = models.TextField(
        'Объяснение',
        blank=True,
        max_length=EXPALANATION_MAX_LEN
    )
    difficulty = models.CharField(
        'Сложность',
        max_length=Difficulty.max_length(),
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM
    )

    class Meta:
        """Мета-класс для вопроса."""

        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['text']

    def __str__(self) -> str:
        """Строковое представление вопроса."""
        return Truncator(self.text).chars(SHORT_STR_LEN)

    def clean(self) -> None:
        """Валидация модели перед сохранением."""
        if self.correct_answer not in self.options:
            raise ValidationError({
                'correct_answer': (
                    f'"{self.correct_answer}" '
                    'нет в вариантах ответов'
                )
            })

    def save(self, *args, **kwargs) -> None:
        """Сохранение модели."""
        self.full_clean()
        super().save(*args, **kwargs)
