# Generated by Django 5.0.1 on 2024-01-16 14:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollabGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('url', models.URLField()),
                ('ingredients', models.JSONField(default=list)),
                ('instructions', models.JSONField(default=list)),
                ('collab_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.collabgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('B', 'Breakfast'), ('L', 'Lunch'), ('D', 'Dinner')], default='B', max_length=1)),
                ('date', models.DateField()),
                ('collab_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.collabgroup')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.recipes')),
            ],
        ),
    ]
