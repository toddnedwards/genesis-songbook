from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('bio/chris-oconnell/', views.chris_oconnell, name='chris_oconnell'),
    path('bio/tony-turrell/', views.tony_turrell, name='tony_turrell'),
    path('bio/todd-nathaniel/', views.todd_nathaniel, name='todd_nathaniel'),
    path('bio/john-lovegrove/', views.john_lovegrove, name='john_lovegrove'),
    path('bio/leon-parr/', views.leon_parr, name='leon_parr'),
    path('bio/', views.bio, name='bio'),
    path('shows/', views.shows, name='shows'),
    path('videos/', views.videos, name='videos'),
    path('photos/', views.photos, name='photos'),
    path('contact/', views.contact, name='contact'),
]