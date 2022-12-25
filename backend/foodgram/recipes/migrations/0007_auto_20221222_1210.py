# Generated by Django 2.2.16 on 2022-12-22 09:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_auto_20221221_1613'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follow',
            new_name='Favorite',
        ),
        migrations.RemoveConstraint(
            model_name='cartlist',
            name='unique favorite recipe',
        ),
        migrations.AddConstraint(
            model_name='cartlist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique cart recipe'),
        ),
    ]