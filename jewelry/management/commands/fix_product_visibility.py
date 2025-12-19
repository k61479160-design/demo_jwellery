from django.core.management.base import BaseCommand
from django.db import transaction
from jewelry.models import Product, ProductCategory, DiamondProduct

class Command(BaseCommand):
    help = 'Fix common product visibility issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix-status',
            action='store_true',
            help='Set all products to active status',
        )
        parser.add_argument(
            '--fix-categories',
            action='store_true',
            help='Assign products to categories if they have none',
        )
        parser.add_argument(
            '--fix-all',
            action='store_true',
            help='Apply all fixes',
        )

    def handle(self, *args, **options):
        if options['fix_all']:
            options['fix_status'] = True
            options['fix_categories'] = True

        with transaction.atomic():
            if options['fix_status']:
                self.fix_product_status()
            
            if options['fix_categories']:
                self.fix_product_categories()

        self.stdout.write(
            self.style.SUCCESS('Product visibility fixes completed successfully!')
        )

    def fix_product_status(self):
        """Set all products to active status"""
        # Fix regular products
        inactive_products = Product.objects.filter(status__in=['inactive', 'out_of_stock', 'discontinued'])
        count = inactive_products.count()
        if count > 0:
            inactive_products.update(status='active')
            self.stdout.write(
                self.style.SUCCESS(f'Fixed status for {count} regular products')
            )

        # Fix diamond products
        unavailable_diamonds = DiamondProduct.objects.filter(status__in=['sold', 'reserved', 'inactive'])
        count = unavailable_diamonds.count()
        if count > 0:
            unavailable_diamonds.update(status='available')
            self.stdout.write(
                self.style.SUCCESS(f'Fixed status for {count} diamond products')
            )

    def fix_product_categories(self):
        """Assign products to categories if they have none"""
        # Get default categories
        default_category = ProductCategory.objects.filter(name='rings').first()
        if not default_category:
            default_category = ProductCategory.objects.filter(is_active=True).first()

        if not default_category:
            self.stdout.write(
                self.style.WARNING('No active categories found. Please create categories first.')
            )
            return

        # Fix regular products without categories
        products_without_categories = Product.objects.filter(categories__isnull=True)
        count = products_without_categories.count()
        if count > 0:
            for product in products_without_categories:
                product.categories.add(default_category)
            self.stdout.write(
                self.style.SUCCESS(f'Assigned {count} products to category: {default_category.display_name}')
            )

        # Fix diamond products without categories
        diamonds_without_categories = DiamondProduct.objects.filter(category__isnull=True)
        count = diamonds_without_categories.count()
        if count > 0:
            diamonds_without_categories.update(category=default_category)
            self.stdout.write(
                self.style.SUCCESS(f'Assigned {count} diamond products to category: {default_category.display_name}')
            ) 