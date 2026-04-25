from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator

class Show(models.Model):
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text="City, Country or State")
    ticket_link = models.URLField(blank=True, null=True, help_text="Link to buy tickets")
    maps_link = models.URLField(blank=True, null=True, help_text="Google Maps link for venue")
    description = models.TextField(blank=True, null=True, help_text="Additional show information")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.date.strftime('%B %d, %Y')} - {self.venue}"
    
    @property
    def is_past(self):
        """Check if show date has passed"""
        return self.date < timezone.now()
    
    @classmethod
    def upcoming_shows(cls):
        """Get all upcoming shows"""
        return cls.objects.filter(date__gte=timezone.now()).order_by('date')


class SEOSettings(models.Model):
    """Global SEO settings for the website"""
    
    # Basic SEO
    site_name = models.CharField(
        max_length=100, 
        default="Genesis Songbook",
        help_text="Your band/site name"
    )
    default_title = models.CharField(
        max_length=60, 
        default="Genesis Songbook - Phil Collins Era Genesis Tribute Band",
        help_text="Default page title (60 chars max)"
    )
    default_description = models.TextField(
        max_length=160,
        default="The ultimate Phil Collins fronted Genesis tribute band. Experience the magic of 80s Genesis with authentic performances of your favorite hits.",
        help_text="Default meta description (160 chars max)",
        validators=[MaxLengthValidator(160)]
    )
    default_keywords = models.TextField(
        default="Genesis tribute band, Phil Collins tribute, 80s music, progressive rock, cover band, tribute show",
        help_text="Comma-separated keywords"
    )
    
    # Location-based SEO
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Your primary location (e.g., 'London', 'New York')"
    )
    
    # Social Media & Open Graph
    og_image = models.URLField(
        blank=True,
        help_text="Default Open Graph image URL (1200x630px recommended)"
    )
    facebook_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True, help_text="Without @")
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Business Info for Local SEO
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website_url = models.URLField(
        default="https://your-domain.com",
        help_text="Your full website URL"
    )
    
    # Advanced SEO
    google_analytics_id = models.CharField(
        max_length=20, 
        blank=True,
        help_text="GA4 Measurement ID (e.g., G-XXXXXXXXXX)"
    )
    google_site_verification = models.CharField(
        max_length=100,
        blank=True,
        help_text="Google Search Console verification code"
    )
    
    # Schema.org structured data
    band_founded_year = models.IntegerField(
        blank=True, 
        null=True,
        help_text="Year the tribute band was founded"
    )
    band_genre = models.CharField(
        max_length=100,
        default="Progressive Rock, Pop Rock, Art Rock",
        help_text="Music genres (comma-separated)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "SEO Settings"
        verbose_name_plural = "SEO Settings"
    
    def __str__(self):
        return f"SEO Settings for {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SEOSettings.objects.exists():
            raise ValueError("Only one SEO settings instance is allowed")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get the SEO settings instance, create if doesn't exist"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Genesis Songbook',
                'default_title': 'Genesis Songbook - Phil Collins Era Genesis Tribute Band',
                'default_description': 'The ultimate Phil Collins fronted Genesis tribute band. Experience the magic of 80s Genesis with authentic performances of your favorite hits.',
            }
        )
        return settings


class PageSEO(models.Model):
    """Page-specific SEO overrides"""
    
    page_slug = models.SlugField(
        unique=True,
        help_text="URL slug for this page (e.g., 'bio', 'shows', 'videos')"
    )
    page_title = models.CharField(
        max_length=60,
        help_text="Custom title for this page (60 chars max)"
    )
    meta_description = models.TextField(
        max_length=160,
        help_text="Custom meta description (160 chars max)",
        validators=[MaxLengthValidator(160)]
    )
    keywords = models.TextField(
        blank=True,
        help_text="Additional keywords specific to this page"
    )
    og_image = models.URLField(
        blank=True,
        help_text="Custom Open Graph image for this page"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Page SEO"
        verbose_name_plural = "Page SEO Settings"
    
    def __str__(self):
        return f"SEO: {self.page_slug}"
