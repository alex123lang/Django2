from django.shortcuts import render
from .models import Product
# Create your views here.


def home(request):
    object_list = Product.objects.all()
    context = {'products': object_list}
    return render(request, 'catalog/product_list.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(name, phone, message)
    return render(request, 'catalog/contact.html')


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)
