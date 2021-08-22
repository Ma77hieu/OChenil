# Generated by Django 3.2 on 2021-08-20 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('administration', '0001_initial'), ('administration', '0002_initial'), ('administration', '0003_alter_dog_dog_age'), ('administration', '0004_size'), ('administration', '0005_auto_20210820_0405')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dog_name', models.CharField(max_length=45)),
                ('dog_age', models.IntegerField()),
                ('dog_race', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(max_length=45)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.box')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.dog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('booking_size', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='administration.size')),
            ],
        ),
        migrations.AddField(
            model_name='box',
            name='box_size',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='administration.size'),
        ),
        migrations.AddField(
            model_name='dog',
            name='dogsize',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='administration.size'),
        ),
        migrations.CreateModel(
            name='Unavailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.box')),
            ],
        ),
    ]