from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json

class Command(BaseCommand):

    @staticmethod
    def json_read_data():
        with open('data.json', 'r') as file:
            data = json.load(file)
        return data

    def handle(self, *args, **options):
        # Удаление всех продуктов и категорий
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание списка для хранения объектов категорий
        category_for_create = []

        # Создание списка для хранения объектов продуктов
        product_for_create = []

        # Обработка данных из JSON
        data = Command.json_read_data()
        for item in data:
            model = item['model']
            fields = item['fields']
            if model == 'catalog.category':
                category_for_create.append(Category(pk=item['pk'], name=fields['name'], description=fields.get('description', '')))
            elif model == 'catalog.product':
                product_for_create.append(
                    Product(
                        pk=item['pk'],
                        name=fields['name'],
                        category_id=fields['category'],
                        description=fields.get('description', ''),
                        photo=fields.get('photo', ''),
                        price=fields.get('price', None),
                        created_at=fields['created_at'],
                        updated_at=fields['updated_at']
                    )
                )

        # Создание объектов категорий в базе данных с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Создание объектов продуктов в базе данных с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with new data'))
