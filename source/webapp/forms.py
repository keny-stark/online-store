from django import forms
from django.forms import widgets
from webapp.models import product_status_choices


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Name')
    description = forms.CharField(max_length=2000, label='Description', widget=widgets.Textarea)
    status = forms.ChoiceField(choices=product_status_choices, label='Status')
    balance = forms.IntegerField(label='Balance', min_value=0)
    price = forms.DecimalField(max_digits=7, label='Price', decimal_places=2)
