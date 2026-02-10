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
                'placeholder': 'Résumé de votre avis (optionnel)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:border-yellow-600 focus:ring-1 focus:ring-yellow-600 outline-none resize-none',
                'placeholder': 'Partagez votre expérience avec ce produit...',
                'rows': 4
            }),
        }
        labels = {
            'rating': 'Votre note',
            'title': 'Titre',
            'comment': 'Votre avis'
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating or rating < 1 or rating > 5:
            raise forms.ValidationError("Veuillez sélectionner une note entre 1 et 5 étoiles.")
        return rating
