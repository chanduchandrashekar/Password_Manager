from django import forms
from .models import SavedPassword

class SavedPasswordForm(forms.ModelForm):
    class Meta:
        model = SavedPassword
        fields = ['site', 'username', 'password']
