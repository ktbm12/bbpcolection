from django import forms
from product.models import Product, ProductImage, Order, Review


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
                "placeholder": "Product Name"
            }),
            "category": forms.Select(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm"
            }),
            "main_image": forms.FileInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 border-dashed rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm cursor-pointer"
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "placeholder": "Price (USD)"
            }),
            "old_price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "placeholder": "Old price (optional)"
            }),
            "stock": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "placeholder": "Stock Quantity"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm",
                "rows": 4,
                "placeholder": "Detailed product description..."
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
                "placeholder": "Alternative text (optional)"
            }),
        }


ProductImageFormSet = forms.inlineformset_factory(
    Product, 
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True
)

class ShippingForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('STRIPE', 'Stripe (Credit Card)'),
        ('PAYPAL', 'PayPal'),
        ('CASH', 'Cash on Delivery'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'hidden'}),
        initial='STRIPE'
    )

    class Meta:
        model = Order
        fields = ['shipping_address', 'shipping_city', 'shipping_phone', 'payment_method']
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-yellow-600 focus:border-transparent outline-none transition',
                'placeholder': 'Full Address (Street, House No, Apt...)',
                'rows': 3
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-yellow-600 focus:border-transparent outline-none transition',
                'placeholder': 'City'
            }),
            'shipping_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-yellow-600 focus:border-transparent outline-none transition',
                'placeholder': 'Phone Number'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)], attrs={
                'class': 'hidden'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-yellow-600 focus:ring-1 focus:ring-yellow-600 outline-none',
                'placeholder': 'Résumé de votre avis (optionnel)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-yellow-600 focus:ring-1 focus:ring-yellow-600 outline-none resize-none',
                'placeholder': 'Partagez votre expérience avec ce produit...',
                'rows': 4
            }),
        }
        labels = {
            'rating': 'Your rating',
            'title': 'Title',
            'comment': 'Your review'
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating or rating < 1 or rating > 5:
            raise forms.ValidationError("Please select a rating between 1 and 5 stars.")
        return rating
