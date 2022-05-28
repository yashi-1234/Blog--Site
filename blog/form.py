from django import forms
from .models import comments
from django.core.exceptions import ValidationError

class CommentForm(forms.ModelForm):
    class Meta:
        model = comments
        exclude = ['post']
         

        