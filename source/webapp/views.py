from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import ProductsModel, product_status_choices
from django.http import HttpResponseNotFound
from webapp.forms import ProductForm


def index_views(request, *args, **kwargs):
    products = ProductsModel.objects.all()
    return render(request, 'index.html', context={
        'articles': products
    })


def product_view(request, pk):
    product = get_object_or_404(ProductsModel, pk=pk)
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
            product = ProductsModel.objects.create(
            description=form.cleaned_data['description'],
            status=form.cleaned_data['status'],
            text=form.cleaned_data['text'],
            created_at=form.cleaned_data['created_at']
            )
            return redirect('article', pk=product.pk)
        else:
            return render(request, 'add_product.html', context={'form': form})


def delete(request, pk):
    product = get_object_or_404(ProductsModel, pk=pk)
    product.delete()
    return redirect('index')


def edit_view(request, pk):
    try:
        products = get_object_or_404(ProductsModel, pk=pk)
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
    except ProductsModel.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")
