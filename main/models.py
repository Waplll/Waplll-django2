from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .validations import validate_image

user_registrated = Signal()


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Активирован")
    fio = models.CharField(max_length=100, blank=True, verbose_name="ФИО")
    is_admin_panel = models.BooleanField(default=False, verbose_name="Доступ к админ панели")

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class CreateRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('inprogress', 'Принято в работу'),
        ('completed', 'Выполнено')
    )
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Название заявки")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Категория", null=True, blank=True)
    photo = models.ImageField(upload_to='photos/%Y%m%d', verbose_name="Фото", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-timestamp']

    def __str__(self):
        return self.title