# urls.py
from django.urls import path, include
from .. import views

urlpatterns = [
    # urls publiques
    path('', views.index, name='index'),  # page d'accueil
    path('client/', include('blog.urls.client_urls')),# URLS spécifiques aux clients
]


