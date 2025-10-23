from django.core.exceptions import ValidationError
def validate_image(image):
    max_size = 2 * 1024 * 1024

    if image.size > max_size:
        raise ValidationError('Размер файла не должен превышать 2 МБ.')

    valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp']

    if not any(image.name.endswith(ext) for ext in valid_extensions):
        raise ValidationError('Разрешены только форматы: jpg, jpeg, png, bmp.')