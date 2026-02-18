from django import forms
from product.models import Review


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
                'placeholder': 'Summary of your review (optional)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-yellow-600 focus:ring-1 focus:ring-yellow-600 outline-none resize-none',
                'placeholder': 'Share your experience with this product...',
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
