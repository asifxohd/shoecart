from django import forms
from django.forms import formset_factory
from .models import SizeVariant, Product  # Assuming you have a SizeVariant model

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # Replace with your actual Product model
        fields = ['name', 'description', 'price', 'discount_price', 'category', 'gender', 'theme_image', 'side_image_1', 'side_image_2', 'side_image_3']

class SizeVariantForm(forms.ModelForm):
    class Meta:
        model = SizeVariant
        fields = ['size', 'quantity']

SizeVariantFormSet = formset_factory(SizeVariantForm, extra=1)
