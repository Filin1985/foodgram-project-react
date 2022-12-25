import re

from django.core.exceptions import ValidationError

ANTI_PATTERN = r'[^\w.@+-]'
REGEX_USERNAME = re.compile(r'^[\w.@+-]+\Z')


def check_username(value):
    """Проверяем, что пользователь не использует имя 'me'."""
    if value == 'me':
        raise ValidationError(
            f'Имя {value} пользователя использовать запрещено!'
        )
    if not REGEX_USERNAME.fullmatch(value):
        result = list(set(re.findall(ANTI_PATTERN, value,)))
        raise ValidationError(
            f"""
            Используйте только цифры, буквы и символы ".@+-".
            Символы {''.join(result)} запрещены.
            """
        )
    return value
