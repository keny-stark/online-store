from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Products, product_status_choices
from django.http import HttpResponseNotFound
from webapp.forms import ProductForm


def index_views(request, *args, **kwargs):
    search = request.GET.get('search', '')
    if search:
        products = Products.objects.filter(name__icontains=search)
    else:
        products = Products.objects.order_by('status', 'name')
    return render(request, 'index.html', context={
        'products': products
    })


def category_view(request, status):
    products = Products.objects.filter(status=status)
    return render(request, 'category_view.html', context={
        'products': products
    })


def product_view(request, pk):
    product = get_object_or_404(Products, pk=pk)
    return render(request, 'product.html', context={
        'product': product})


def add_product(request, *args, **kwargs):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'add_product.html', context={
            'form': form,
            'product_status_choices': product_status_choices
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Products.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            status=form.cleaned_data['status'],
            balance=form.cleaned_data['balance'],
            price=form.cleaned_data['price']
            )
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'add_product.html', context={'form': form})


def delete_product(request, pk):
    product = get_object_or_404(Products, pk=pk)
    product.delete()
    return redirect('index')


def update_product(request, pk):
    try:
        products = get_object_or_404(Products, pk=pk)
        if request.method == 'GET':
            form = ProductForm(data={
                'name': products.name,
                'description': products.description,
                'status': products.status,
                'balance': products.balance,
                'price': products.price
            })
            return render(request, 'edit.html', context={
                'products': products, 'form': form})
        elif request.method == "POST":
            form = ProductForm(data=request.POST)
            if form.is_valid():
                products.name = form.cleaned_data['name']
                products.description = form.cleaned_data['description']
                products.status = form.cleaned_data['status']
                products.balance = form.cleaned_data['balance']
                products.price = form.cleaned_data['price']
                products.save()
                return redirect('product_view', pk=products.pk)
            else:
                return render(request, 'edit.html', context={'form': form, 'products': products})
    except Products.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")
