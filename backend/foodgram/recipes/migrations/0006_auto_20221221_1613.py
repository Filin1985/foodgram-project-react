# Generated by Django 2.2.16 on 2022-12-21 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_auto_20221215_2029'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavoritesList',
            new_name='Follow',
        ),
        migrations.AlterField(
            model_name='ingredientquantity',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='recipes.Ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='ingredientquantity',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
    ]