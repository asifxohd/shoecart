from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    size = forms.CharField(max_length=10, required=False)  # Add the size field
    class Meta:
        model = Product
        fields = '__all__'  # This will include all fields in the form
