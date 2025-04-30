from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_client(user):
    return user.user_type == 'client'

@user_passes_test(is_client)
def dashboard_client(request):
    return render(request, 'magazin_vente_velo/dashboard_client.html')