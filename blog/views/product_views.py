# views/product_views.py
from django.shortcuts import render
from models import products

def product_list(request):
    products = products.objects.all()
    if not products:
        return render(request, 'magazin_vente_velo/product_not_found.html', status=404)
    return render(request, 'magazin_vente_velo/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = products.objects.get(id=product_id)
    if not product:
        return render(request, 'magazin_vente_velo/product_not_found.html', status=404)
    return render(request, 'magazin_vente_velo/product_detail.html', {'product': product})
