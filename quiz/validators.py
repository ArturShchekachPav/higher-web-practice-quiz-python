from django.core.exceptions import ValidationError


def validate_options(value: any) -> None:
    """Валидатор для options вопроса"""

    if not isinstance(value, list):
        raise ValidationError('Options должен быть списком')

    if len(value) < 2:
        raise ValidationError('Должно быть минимум 2 варианта ответа')

    for item in value:
        if not isinstance(item, str):
            raise ValidationError(
                'Все варианты ответов должны быть строками'
            )
