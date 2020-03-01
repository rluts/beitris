# Generated by Django 3.0.3 on 2020-02-24 23:15

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wikidata_parent_entity', models.CharField(blank=True, max_length=35, null=True)),
                ('name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.BigIntegerField()),
                ('backend', models.CharField(choices=[('api', 'API'), ('tg', 'Telegram')], max_length=10)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('started', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Category')),
                ('initiator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_name', to=settings.AUTH_USER_MODEL)),
                ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participants_games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('wikidata_id', models.CharField(max_length=35)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Category')),
            ],
            options={
                'unique_together': {('category', 'wikidata_id'), ('category', 'name')},
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('question_wikidata_prop', models.CharField(blank=True, max_length=35, null=True)),
                ('type', models.CharField(choices=[('image', 'IMAGE'), ('text', 'TEXT'), ('sound', 'SOUND'), ('coords', 'SOUND')], max_length=10)),
                ('is_question_in_child', models.BooleanField(default=False)),
                ('child_prop', models.CharField(blank=True, max_length=35, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.BigIntegerField()),
                ('ask_date', models.DateTimeField(auto_now_add=True)),
                ('right_answers', django.contrib.postgres.fields.jsonb.JSONField()),
                ('associated_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Game')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to='quiz.Object')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
