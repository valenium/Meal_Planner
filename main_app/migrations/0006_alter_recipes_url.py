# Generated by Django 5.0.1 on 2024-01-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_meal_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
