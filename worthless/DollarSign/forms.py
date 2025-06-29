from django import forms
from .models import Stock
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# User Registration Form
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker', 'shares', 'purchase_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_ticker(self):
        ticker = self.cleaned_data.get('ticker', '').upper()
        if not ticker:
            raise forms.ValidationError("The ticker symbol cannot be empty.")
        return ticker
