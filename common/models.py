from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    external_id = models.BigIntegerField(null=True, blank=True)
    backend = models.CharField(null=True, blank=True, max_length=10)


class Factory(models.Model):
    class Meta:
        verbose_name_plural = 'Factories'

    category_name = models.CharField(max_length=50)
    language = models.CharField(max_length=3, default='en')

    def __str__(self):
        return self.category_name


class FactoryFilter(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    property = models.CharField(max_length=35)
    entity = models.CharField(max_length=35)

    def __str__(self):
        return f'{self.property}, {self.entity}'


class Alias(models.Model):
    class Meta:
        verbose_name_plural = 'Aliases'
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    property = models.CharField(max_length=35)

    def __str__(self):
        return self.property