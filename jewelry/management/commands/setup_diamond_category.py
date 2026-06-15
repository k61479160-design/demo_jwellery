from django.core.management.base import BaseCommand
from jewelry.models import ProductCategory, DiamondProduct


class Command(BaseCommand):
    help = 'Setup diamond category and ensure diamond products are properly categorized'

    def handle(self, *args, **options):
        # Create diamond category if it doesn't exist
        diamond_category, created = ProductCategory.objects.get_or_create(
            name='diamonds',
            defaults={
                'display_name': 'Diamonds',
                'description': 'Premium diamond collection',
                'icon': 'diamond',
                'sort_order': 5,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created diamond category: {diamond_category.display_name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Diamond category already exists: {diamond_category.display_name}')
            )
        
        # Update diamond products to have the diamond category
        diamond_products = DiamondProduct.objects.filter(category__isnull=True)
        updated_count = diamond_products.update(category=diamond_category)
        
        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Updated {updated_count} diamond products with diamond category')
            )
        else:
            self.stdout.write(
                self.style.WARNING('No diamond products needed category update')
            )
        
        # Show summary
        total_diamonds = DiamondProduct.objects.count()
        diamonds_with_category = DiamondProduct.objects.filter(category__isnull=False).count()
        
        self.stdout.write(
            self.style.SUCCESS(f'Total diamond products: {total_diamonds}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Diamond products with category: {diamonds_with_category}')
        ) 