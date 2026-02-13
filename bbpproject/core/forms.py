from django import forms
from .models import LegalPage

class LegalPageForm(forms.ModelForm):
    class Meta:
        model = LegalPage
        fields = ['title', 'slug', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm',
                'placeholder': 'Page Title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm',
                'placeholder': 'page-slug'
            }),
            'content': forms.Textarea(attrs={
                'class': 'ckeditor w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-yellow-600 focus:outline-none transition-all duration-300 bg-white/50 backdrop-blur-sm',
                'id': 'editor'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-gray-200 text-yellow-600 focus:ring-yellow-600 transition-all duration-300'
            }),
        }
