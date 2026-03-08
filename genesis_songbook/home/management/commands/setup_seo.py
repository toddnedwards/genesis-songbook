"""
Management command to set up initial SEO data for Genesis tribute band
"""
from django.core.management.base import BaseCommand
from home.models import SEOSettings, PageSEO


class Command(BaseCommand):
    help = 'Set up initial SEO data optimized for Genesis tribute band'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--location',
            type=str,
            help='Your primary location (e.g., "London", "New York")',
        )
        parser.add_argument(
            '--website-url',
            type=str,
            help='Your website URL (e.g., "https://your-domain.com")',
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Setting up SEO data for Genesis tribute band...')
        
        # Create or update global SEO settings
        seo_settings, created = SEOSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Genesis Songbook',
                'default_title': 'Genesis Songbook - Premier Phil Collins Era Genesis Tribute Band',
                'default_description': 'Experience the ultimate Phil Collins fronted Genesis tribute band. Authentic performances of 80s Genesis hits including "In The Air Tonight", "Against All Odds" and more.',
                'default_keywords': 'Genesis tribute band, Phil Collins tribute, 80s music, progressive rock, cover band, tribute show, Genesis cover band, Phil Collins era Genesis',
                'location': options.get('location', ''),
                'website_url': options.get('website_url', 'https://your-domain.com'),
                'band_founded_year': 2020,  # Update this to your actual founding year
                'band_genre': 'Progressive Rock, Pop Rock, Art Rock, New Wave',
            }
        )
        
        action = 'Created' if created else 'Updated'
        self.stdout.write(f'{action} global SEO settings')
        
        # Create page-specific SEO data
        page_seo_data = [
            {
                'page_slug': 'bio',
                'page_title': 'Band Biography - Genesis Songbook Tribute Band',
                'meta_description': 'Meet the talented musicians behind Genesis Songbook, the premier Phil Collins era Genesis tribute band dedicated to authentic performances.',
                'keywords': 'Genesis tribute band biography, Phil Collins tribute musicians, Genesis cover band members, tribute band history',
            },
            {
                'page_slug': 'shows',
                'page_title': 'Upcoming Shows - Genesis Songbook Tour Dates',
                'meta_description': 'Find Genesis Songbook tribute band tour dates, upcoming concerts and ticket information. Experience live Genesis hits performed authentically.',
                'keywords': 'Genesis tribute band tour dates, Phil Collins tribute concerts, Genesis cover band shows, tribute band tickets',
            },
            {
                'page_slug': 'videos',
                'page_title': 'Performance Videos - Genesis Songbook Live',  
                'meta_description': 'Watch Genesis Songbook perform classic Genesis and Phil Collins hits. See why we are the leading Phil Collins era Genesis tribute band.',
                'keywords': 'Genesis tribute band videos, Phil Collins tribute performances, Genesis cover band live, tribute band concert footage',
            },
            {
                'page_slug': 'photos',
                'page_title': 'Photo Gallery - Genesis Songbook Tribute Band',
                'meta_description': 'Browse photos of Genesis Songbook performances, behind-the-scenes moments and tribute band memories from our Genesis tribute shows.',
                'keywords': 'Genesis tribute band photos, Phil Collins tribute images, Genesis cover band gallery, tribute band pictures',
            },
            {
                'page_slug': 'index',
                'page_title': 'Genesis Songbook - #1 Phil Collins Era Genesis Tribute Band',
                'meta_description': 'The ultimate Phil Collins fronted Genesis tribute band. Book us for authentic performances of "In The Air Tonight", "Invisible Touch", "Against All Odds" and more Genesis classics.',
                'keywords': 'best Genesis tribute band, Phil Collins tribute band, Genesis cover band, hire tribute band, book Genesis tribute, Phil Collins era Genesis',
            },
        ]
        
        created_pages = 0
        updated_pages = 0
        
        for page_data in page_seo_data:
            page_seo, created = PageSEO.objects.get_or_create(
                page_slug=page_data['page_slug'],
                defaults=page_data
            )
            if created:
                created_pages += 1
            else:
                # Update existing pages with new data
                for key, value in page_data.items():
                    setattr(page_seo, key, value)
                page_seo.save()
                updated_pages += 1
                
        self.stdout.write(f'Created {created_pages} new page SEO entries')
        self.stdout.write(f'Updated {updated_pages} existing page SEO entries')
        
        # Success message with helpful tips
        self.stdout.write(
            self.style.SUCCESS(
                '\nSEO setup complete! \n\n'
                'Next steps for maximum SEO success:\n'
                '1. Visit Django Admin -> SEO Settings to customize your details\n'
                '2. Add your Google Analytics ID and Search Console verification\n'
                '3. Upload high-quality images (1200x630px) for social sharing\n'
                '4. Add your actual location and contact details\n'
                '5. Customize page-specific SEO in Django Admin -> Page SEO\n'
                '6. Create quality content with Genesis and Phil Collins keywords\n'
                '7. Get backlinks from music venues, event listings, and local directories\n'
                '8. Regularly update your show listings and band news\n'
                '9. Encourage fan reviews and testimonials\n'
                '10. Share content on social media to build engagement'
            )
        )