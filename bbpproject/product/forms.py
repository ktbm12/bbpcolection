from django import forms
from product.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "main_image",
            "price",
            "old_price",
            "stock",
            "is_featured",
            "description",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
