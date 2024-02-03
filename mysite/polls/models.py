from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.dispatch import Signal
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return 'mysite/file'.join([get_random_string(5) + '_' + filename])

class Service(models.Model):
    service_name = models.CharField(max_length=200, verbose_name='Название услуги/товара')
    service_date = models.DateTimeField('Дата публикации')
    description_service = models.CharField(max_length=200, verbose_name='Краткое описание')
    service_img = models.ImageField(verbose_name='Картинка', upload_to=get_name_file, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    user = models.ForeignKey('User', verbose_name='Пользователь',on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.service_name

class User(AbstractUser):
    username = models.CharField(max_length=200, verbose_name='Логин', unique=True, blank=False, validators=[
        RegexValidator(
            regex='^[A-Za-z -]*$',
            message='Имя пользователя должно состоять только из латиницы',
            code='invalid_username'
        ),
    ])
    avatar = models.ImageField(upload_to=get_name_file, verbose_name='Аватар', blank=False, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    password = models.CharField(max_length=200, verbose_name='Пароль', blank=False)

    class Meta:
        ordering = ['username', 'avatar', 'password']

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


user_registrated = Signal()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ordered_services = models.ManyToManyField(Service)

class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.service.service_name}"


