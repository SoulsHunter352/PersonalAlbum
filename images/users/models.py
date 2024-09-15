from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """
    Расширение модели пользователя.
    Добавлено поле фотографии, показывать ли почту в профиле
    """
    photo = models.ImageField(verbose_name='Фотография', upload_to='users', blank=True, null=True)
    public_email = models.BooleanField(verbose_name='Отобразить почту', default=True)