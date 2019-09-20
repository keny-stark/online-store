from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import ProductsModel, product_status_choices
from django.http import HttpResponseNotFound
from webapp.forms import ProductForm


def index_views(request, *args, **kwargs):
    articles = ProductsModel.objects.all()
    return render(request, 'index.html', context={
        'articles': articles
    })


def product_view(request, pk):
    article = get_object_or_404(ProductsModel, pk=pk)
    return render(request, 'product.html', context={
        'article': article})


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
            article = ProductsModel.objects.create(
            description=form.cleaned_data['description'],
            status=form.cleaned_data['status'],
            text=form.cleaned_data['text'],
            created_at=form.cleaned_data['created_at']
            )
            return redirect('article', pk=article.pk)
        else:
            return render(request, 'add_product.html', context={'form': form})


def delete(request, pk):
    article = get_object_or_404(ProductsModel, pk=pk)
    article.delete()
    return redirect('index')


def edit_view(request, pk):
    try:
        articles = get_object_or_404(ProductsModel, pk=pk)
        if request.method == 'GET':
            form = ProductForm(data={
                'description': articles.description,
                'status': articles.status,
                'text': articles.text,
                'created_at': articles.created_at
            })
            return render(request, 'edit.html', context={
                'articles': articles, 'form': form})
        elif request.method == "POST":
            form = ProductForm(data=request.POST)
            if form.is_valid():
                articles.description = form.cleaned_data['description']
                articles.status = form.cleaned_data['status']
                articles.text = form.cleaned_data['text']
                articles.created_at = form.cleaned_data['created_at']
                articles.save()
                return redirect('article', pk=articles.pk)
            else:
                return render(request, 'edit.html', context={'form': form, 'articles': articles})
    except ProductsModel.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")
