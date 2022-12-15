from django.core.exceptions import ValidationError
from django.utils import timezone


def validate(title_year):
    now_year = timezone.now().year
    if title_year > now_year or title_year <= 0:
        raise ValidationError('Пожалуйста, проверьте правильность года!')
