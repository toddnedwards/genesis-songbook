"""
Context processors to make SEO data globally available in templates
"""
from django.http import HttpRequest
from .models import SEOSettings, PageSEO


def seo_context(request: HttpRequest):
    """
    Make SEO settings available in all templates
    """
    # Get global SEO settings
    seo_settings = SEOSettings.get_settings()
    
    # Try to get page-specific SEO if available
    page_seo = None
    if hasattr(request, 'resolver_match') and request.resolver_match:
        # Extract URL name for page-specific SEO
        url_name = request.resolver_match.url_name
        if url_name:
            try:
                page_seo = PageSEO.objects.get(page_slug=url_name)
            except PageSEO.DoesNotExist:
                pass
    
    # Build context with fallbacks
    context = {
        'seo_settings': seo_settings,
        'page_seo': page_seo,
        'seo_title': page_seo.page_title if page_seo else seo_settings.default_title,
        'seo_description': page_seo.meta_description if page_seo else seo_settings.default_description,
        'seo_keywords': f"{seo_settings.default_keywords}, {page_seo.keywords}" if page_seo and page_seo.keywords else seo_settings.default_keywords,
        'seo_og_image': page_seo.og_image if page_seo and page_seo.og_image else seo_settings.og_image,
    }
    
    return context