# Generated by Django 3.0.3 on 2020-02-28 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alias_factory_factoryfilter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alias',
            options={'verbose_name_plural': 'Aliases'},
        ),
        migrations.AlterModelOptions(
            name='factory',
            options={'verbose_name_plural': 'Factories'},
        ),
    ]