# Generated by Django 3.0.3 on 2020-05-01 17:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_gametable_current_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='response_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]