from django.contrib import admin
from django import forms
from .models import Show, SEOSettings, PageSEO

class ShowAdminForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'
        widgets = {
            'date': forms.SplitDateTimeWidget(
                date_attrs={'type': 'date'},
                time_attrs={'type': 'time', 'step': '1800'}  # 30 minutes
            )
        }

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    form = ShowAdminForm
    list_display = ('date', 'venue', 'location', 'has_ticket_link', 'is_past')
    list_filter = ('date', 'location')
    search_fields = ('venue', 'location', 'description')
    date_hierarchy = 'date'
    ordering = ['-date']
    
    fieldsets = (
        ('Show Information', {
            'fields': ('date', 'venue', 'location'),
            'description': 'Select date and time for the show. Times can be selected in 30-minute intervals.'
        }),
        ('Ticketing', {
            'fields': ('ticket_link', 'maps_link', 'apple_maps_link'),
            'description': 'Add ticket URL, Google Maps and Apple Maps links for the venue'
        }),
        ('Additional Details', {
            'fields': ('description',),
            'classes': ('collapse',)
        })
    )
    
    def has_ticket_link(self, obj):
        """Display if show has ticket link"""
        return bool(obj.ticket_link)
    has_ticket_link.boolean = True
    has_ticket_link.short_description = 'Tickets Available'
    
    def is_past(self, obj):
        """Display if show is in the past"""
        return obj.is_past
    is_past.boolean = True
    is_past.short_description = 'Past Show'

@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        return not SEOSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of SEO settings  
        return False
    
    fieldsets = (
        ('Basic SEO', {
            'fields': ('site_name', 'default_title', 'default_description', 'default_keywords'),
            'description': 'Core SEO settings that apply to all pages by default.'
        }),
        ('Location & Business', {
            'fields': ('location', 'phone', 'email', 'website_url'),
            'description': 'Business information for local SEO and contact details.'
        }),
        ('Social Media', {
            'fields': ('og_image', 'facebook_url', 'twitter_handle', 'instagram_url', 'youtube_url'),
            'description': 'Social media profiles and Open Graph image.'
        }),
        ('Band Information', {
            'fields': ('band_founded_year', 'band_genre'),
            'description': 'Information about your Genesis tribute band for structured data.'
        }),
        ('Advanced SEO', {
            'fields': ('google_analytics_id', 'google_site_verification'),
            'description': 'Google Analytics and Search Console integration.',
            'classes': ('collapse',)
        })
    )
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to edit form if settings exist, otherwise show add form"""
        if SEOSettings.objects.exists():
            settings = SEOSettings.objects.first()
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse('admin:home_seosettings_change', args=[settings.pk]))
        return super().changelist_view(request, extra_context)


@admin.register(PageSEO)
class PageSEOAdmin(admin.ModelAdmin):
    list_display = ('page_slug', 'page_title', 'meta_description_preview', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('page_slug', 'page_title', 'meta_description')
    
    fieldsets = (
        ('Page Identification', {
            'fields': ('page_slug',),
            'description': 'Enter the URL slug for the page (e.g., \"bio\", \"shows\", \"videos\")'
        }),
        ('SEO Content', {
            'fields': ('page_title', 'meta_description', 'keywords'),
            'description': 'Custom SEO content for this specific page.'
        }),
        ('Social Sharing', {
            'fields': ('og_image',),
            'description': 'Custom image for social media sharing (optional).'
        })
    )
    
    def meta_description_preview(self, obj):
        """Show truncated meta description"""
        if len(obj.meta_description) > 50:
            return f"{obj.meta_description[:50]}..."
        return obj.meta_description
    meta_description_preview.short_description = 'Description Preview'