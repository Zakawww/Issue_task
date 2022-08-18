from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Profile(models.Model):
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name='Аватар')
    url_user = models.URLField(max_length=200, null=True, blank=True, verbose_name='Ссылка')
    about_user = models.TextField(max_length=1000, null=True, blank=True, verbose_name='О себе')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь',
                                related_name='profile')


