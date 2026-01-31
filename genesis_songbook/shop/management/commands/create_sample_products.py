from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Create sample products for the store'

    def handle(self, *args, **options):
        # Create categories
        merchandise_category, created = Category.objects.get_or_create(
            name='Merchandise',
            defaults={'slug': 'merchandise'}
        )
        
        music_category, created = Category.objects.get_or_create(
            name='Music',
            defaults={'slug': 'music'}
        )

        # Create sample products
        products = [
            {
                'name': 'Genesis Songbook T-Shirt',
                'slug': 'genesis-songbook-t-shirt',
                'category': merchandise_category,
                'description': 'Official Genesis Songbook band t-shirt. High quality cotton blend with the band logo printed on the front. Available in black.',
                'price': 25.00,
                'stock': 50,
                'is_clothing': True,
            },
            {
                'name': 'Genesis Songbook Hoodie',
                'slug': 'genesis-songbook-hoodie',
                'category': merchandise_category,
                'description': 'Comfortable hoodie featuring the Genesis Songbook logo. Perfect for concerts or casual wear. Premium quality fleece material.',
                'price': 45.00,
                'stock': 30,
                'is_clothing': True,
            },
            {
                'name': 'Genesis Tribute Mug',
                'slug': 'genesis-tribute-mug',
                'category': merchandise_category,
                'description': 'Start your day with Genesis! Ceramic mug featuring classic Genesis album artwork and Genesis Songbook branding.',
                'price': 15.00,
                'stock': 75,
                'is_clothing': False,
            },
            {
                'name': 'Live Performance USB',
                'slug': 'live-performance-usb',
                'category': music_category,
                'description': 'USB drive containing exclusive live recordings from Genesis Songbook performances. High quality audio recordings.',
                'price': 35.00,
                'stock': 25,
                'is_clothing': False,
            },
            {
                'name': 'Genesis Songbook Tote Bag',
                'slug': 'genesis-songbook-tote-bag',
                'category': merchandise_category,
                'description': 'Eco-friendly canvas tote bag with Genesis Songbook logo. Perfect for shopping or carrying your Genesis memorabilia.',
                'price': 18.00,
                'stock': 40,
                'is_clothing': False,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created product: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed!')
        )