from django.core.validators import URLValidator


def validate_url(value):
    url_validation = URLValidator(message='Not a valid URL!')
    if value.startswith('http'):
        url_validation(value)
    else:
        value = 'http://' + value
        url_validation(value)
    return value
