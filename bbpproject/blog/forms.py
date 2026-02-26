from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-gold-500 focus:ring-0 transition-all outline-none',
                'placeholder': 'Enter post title'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-gold-500 focus:ring-0 transition-all outline-none',
                'rows': 3,
                'placeholder': 'Enter short summary for homepage'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-gold-500 focus:ring-0 transition-all outline-none',
                'rows': 10,
                'placeholder': 'Write your content here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-gold-500 focus:ring-0 transition-all outline-none'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-gray-300 text-gold-600 focus:ring-gold-500'
            }),
        }
