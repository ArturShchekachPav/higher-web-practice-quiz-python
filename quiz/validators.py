from django.core.exceptions import ValidationError

from quiz.constants import MIN_OPTIONS_CHOICES_COUNT


def validate_options(value: any) -> None:
    """Валидатор для options вопроса"""

    if not isinstance(value, list):
        raise ValidationError('Options должен быть списком')

    if len(value) < MIN_OPTIONS_CHOICES_COUNT:
        raise ValidationError(
            (
                'Должно быть минимум '
                f'{MIN_OPTIONS_CHOICES_COUNT} варианта ответа'
            )
        )

    for item in value:
        if not isinstance(item, str):
            raise ValidationError(
                'Все варианты ответов должны быть строками'
            )
