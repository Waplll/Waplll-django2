from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

user_registrated = Signal(['instance'])

class AdvUser(AbstractUser):
   is_activated = models.BooleanField(default=True, db_index=True,verbose_name='Прошел активацию?')
   fio = models.CharField(max_length=100, blank=True, verbose_name='ФИО')

   class Meta(AbstractUser.Meta):
       pass