from django.core.management.base import BaseCommand
from jewelry.models import Product, ProductCategory


class Command(BaseCommand):
    help = 'Check and ensure gold products are properly categorized'

    def handle(self, *args, **options):
        # Get all categories
        categories = ProductCategory.objects.all()
        self.stdout.write(f'Available categories: {[c.name for c in categories]}')
        
        # Check products with gold metal type
        gold_products = Product.objects.filter(
            metal_type__in=['yellow_gold', 'white_gold', 'rose_gold'],
            status='active'
        )
        
        self.stdout.write(f'Total gold products: {gold_products.count()}')
        
        for product in gold_products:
            self.stdout.write(f'Product: {product.name} - Metal: {product.get_metal_type_display()} - Categories: {[c.name for c in product.categories.all()]}')
        
        # Check products without categories
        products_without_categories = Product.objects.filter(
            categories__isnull=True,
            status='active'
        )
        
        self.stdout.write(f'Products without categories: {products_without_categories.count()}')
        
        for product in products_without_categories:
            self.stdout.write(f'Product without category: {product.name} - Metal: {product.get_metal_type_display()}')
        
        # Show all active products
        all_active_products = Product.objects.filter(status='active')
        self.stdout.write(f'Total active products: {all_active_products.count()}')
        
        for product in all_active_products:
            categories_list = [c.name for c in product.categories.all()]
            self.stdout.write(f'Product: {product.name} - Categories: {categories_list}') 