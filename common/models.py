from django.contrib.auth.models import AbstractUser
from django.db import models


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
    default_language = models.CharField(max_length=3, default='en')
    is_online = models.BooleanField(default=False)
    current_channel = models.CharField(null=True, blank=True, max_length=255)

    def get_full_name(self):
        return super(User, self).get_full_name() or self.email or self.username


class Factory(models.Model):
    class Meta:
        verbose_name_plural = 'Factories'

    category_name = models.CharField(max_length=50)
    language = models.CharField(max_length=3, default='en')
    query = models.TextField(null=True, blank=True,
                             help_text='https://query.wikidata.org/')

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