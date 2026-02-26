"""Утилиты для работы с моделями."""

from typing import Any, Dict, TypeVar

ModelType = TypeVar('ModelType')


def update_model_instance(
    instance: ModelType, data: Dict[str, Any]
) -> ModelType:
    """Обновить поля модели из словаря."""
    for key, value in data.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
    instance.save()
    return instance
