from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('bio/chris-oconnell/', views.chris_oconnell, name='chris_oconnell'),
    path('bio/', views.bio, name='bio'),
    path('shows/', views.shows, name='shows'),
    path('videos/', views.videos, name='videos'),
    path('photos/', views.photos, name='photos'),
    path('contact/', views.contact, name='contact'),
]