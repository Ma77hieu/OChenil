# Generated by Django 3.2.6 on 2021-08-23 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='box',
            name='box_size',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='administration.size'),
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_size',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='administration.size'),
        ),
        migrations.AddField(
            model_name='booking',
            name='box',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.box'),
        ),
        migrations.AddField(
            model_name='booking',
            name='dog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.dog'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
