from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

    rating = forms.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        min_value=0, 
        max_value=5,
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )
    
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40})  
    )