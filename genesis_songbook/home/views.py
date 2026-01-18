from django.shortcuts import render

def home(request):
    """Home page view."""
    return render(request, 'index.html')


def bio(request):
    """Bio page view."""
    return render(request, 'bio.html')


def shows(request):
    """Shows page view."""
    return render(request, 'shows.html')


def photos(request):
    """Photos page view."""
    return render(request, 'photos.html')


def videos(request):
    """Videos page view."""
    return render(request, 'videos.html')