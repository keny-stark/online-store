from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Products, product_status_choices
from django.http import HttpResponseNotFound
from webapp.forms import ProductForm
from django.db.models import Q


def index_views(request, *args, **kwargs):
    search = request.GET.get('search', '')
    if search:
        products = Products.objects.filter(Q(name=search))
    else:
        products = Products.objects.order_by('name')
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
        'article': product})


def add_product(request, *args, **kwargs):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product.html', context={
            'form': form,
            'product_status_choices': product_status_choices
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Products.objects.create(
            description=form.cleaned_data['description'],
            status=form.cleaned_data['status'],
            text=form.cleaned_data['text'],
            created_at=form.cleaned_data['created_at']
            )
            return redirect('article', pk=product.pk)
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
                'description': products.description,
                'status': products.status,
                'text': products.text,
                'created_at': products.created_at
            })
            return render(request, 'edit.html', context={
                'articles': products, 'form': form})
        elif request.method == "POST":
            form = ProductForm(data=request.POST)
            if form.is_valid():
                products.description = form.cleaned_data['description']
                products.status = form.cleaned_data['status']
                products.text = form.cleaned_data['text']
                products.created_at = form.cleaned_data['created_at']
                products.save()
                return redirect('article', pk=products.pk)
            else:
                return render(request, 'edit.html', context={'form': form, 'articles': products})
    except Products.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")
