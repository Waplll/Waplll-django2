from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .validations import validate_image

user_registrated = Signal(['instance'])

class AdvUser(AbstractUser):
   is_activated = models.BooleanField(default=True, db_index=True,verbose_name='Прошел активацию?')
   fio = models.CharField(max_length=100, blank=True, verbose_name='ФИО')
   class Meta(AbstractUser.Meta):
       pass




class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return self.name

class CreateRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    )
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото помещения', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Временная метка')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    def __str__(self):
        return self.title