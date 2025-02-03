from django import forms
from .models import Review

# in progress, not idk if this works yet

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment',)