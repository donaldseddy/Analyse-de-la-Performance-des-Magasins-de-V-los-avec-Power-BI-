from django.urls import path
from ..views import client_views

app_name = 'client'  # permet de nommer les routes comme 'client:dashboard'

urlpatterns = [
    path('dashboard/', client_views.dashboard_client, name='dashboard'),
    #path('mes-commandes/', client_views.client_orders, name='mes_commandes'),
    #path('mon-profil/', client_views.client_profile, name='mon_profil'),
]
