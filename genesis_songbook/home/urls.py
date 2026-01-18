from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('bio/', views.bio, name='bio'),
    path('shows/', views.shows, name='shows'),
    path('videos/', views.videos, name='videos'),
    path('photos/', views.photos, name='photos'),
]