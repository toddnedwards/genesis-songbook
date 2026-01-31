from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
from .models import Show

def home(request):
    """Home page view."""
    return render(request, 'index.html')


def bio(request):
    """Bio page view."""
    return render(request, 'bio.html')


def shows(request):
    """Shows page view with monthly categorization."""
    # Get all upcoming shows
    upcoming_shows = Show.upcoming_shows()
    
    # Group shows by month/year
    shows_by_month = defaultdict(list)
    
    # Group shows by their month/year
    for show in upcoming_shows:
        # Create month key as first day of the month
        month_key = show.date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        shows_by_month[month_key].append(show)
    
    # Only create monthly_shows for months that actually have shows
    monthly_shows = []
    for month_date in sorted(shows_by_month.keys()):
        month_shows = shows_by_month[month_date]
        monthly_shows.append({
            'month_date': month_date,
            'month_name': month_date.strftime('%B %Y'),
            'shows': month_shows,
            'has_shows': True  # We only include months with shows
        })
    
    context = {
        'monthly_shows': monthly_shows,
        'has_any_shows': len(monthly_shows) > 0
    }
    return render(request, 'shows.html', context)


def photos(request):
    """Photos page view."""
    return render(request, 'photos.html')


def videos(request):
    """Videos page view."""
    return render(request, 'videos.html')