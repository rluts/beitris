# Generated by Django 3.0.3 on 2020-05-01 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_answer_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='gametable',
            name='current_question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.Question'),
        ),
    ]