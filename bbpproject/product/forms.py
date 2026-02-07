from django import forms
from product.models import Product, ProductImage


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
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "placeholder": "Nom du produit"
            }),
            "category": forms.Select(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm"
            }),
            "main_image": forms.FileInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 border-dashed rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm cursor-pointer"
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "placeholder": "Prix (FCFA)"
            }),
            "old_price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "placeholder": "Ancien prix (facultatif)"
            }),
            "stock": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "placeholder": "Quantité en stock"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "rows": 4,
                "placeholder": "Description détaillée du produit..."
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "w-5 h-5 rounded border-gray-200 text-yellow-600 focus:ring-yellow-600 transition-all duration-300"
            }),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']
        widgets = {
            "image": forms.FileInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 border-dashed rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm cursor-pointer"
            }),
            "alt_text": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "placeholder": "Texte alternatif (facultatif)"
            }),
        }


ProductImageFormSet = forms.inlineformset_factory(
    Product, 
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True
)
