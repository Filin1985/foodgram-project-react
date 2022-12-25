import csv
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient

FILES_DIR = '../../data'


class Command(BaseCommand):
    """
    Загрузка ингредиентов в базу
    """
    help = 'Load ingredients from csv or json file to your database'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            default='ingredients.csv',
            nargs='?',
            type=str
        )

    def handle(self, *args, **options):
        with open(os.path.join(FILES_DIR, options['filename']), 'r',
                  encoding='utf-8') as file:
            data = csv.reader(file)
            for row in data:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
