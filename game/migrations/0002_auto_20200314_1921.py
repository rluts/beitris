# Generated by Django 3.0.3 on 2020-03-14 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gametable',
            name='max_participant',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='gametable',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='game.Room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='backend',
            field=models.CharField(choices=[('telegram', 'telegram'), ('api', 'api')], max_length=10),
        ),
    ]