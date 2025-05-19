from django import forms
from django.contrib.auth import get_user_model
from .models import Wallet, Currency

User = get_user_model()

class DepositForm(forms.Form):
    currency    = forms.ModelChoiceField(
                      queryset=Currency.objects.all(),
                      widget=forms.Select(attrs={'class':'form-select'})
                  )
    amount      = forms.DecimalField(
                      max_digits=12, decimal_places=2, min_value=0.01,
                      widget=forms.NumberInput(attrs={
                          'class':'form-control', 'placeholder':'Amount'
                      })
                  )
    description = forms.CharField(
                      required=False, max_length=255,
                      widget=forms.TextInput(attrs={
                          'class':'form-control',
                          'placeholder':'Description (optional)'
                      })
                  )

class WithdrawalForm(forms.Form):
    currency    = forms.ModelChoiceField(
                      queryset=Currency.objects.all(),
                      widget=forms.Select(attrs={'class':'form-select'})
                  )
    amount      = forms.DecimalField(
                      max_digits=12, decimal_places=2, min_value=0.01,
                      widget=forms.NumberInput(attrs={
                          'class':'form-control', 'placeholder':'Amount'
                      })
                  )
    description = forms.CharField(
                      required=False, max_length=255,
                      widget=forms.TextInput(attrs={
                          'class':'form-control',
                          'placeholder':'Description (optional)'
                      })
                  )

class TransferForm(forms.Form):
    currency    = forms.ModelChoiceField(
                      queryset=Currency.objects.all(),
                      widget=forms.Select(attrs={'class':'form-select'})
                  )
    recipient   = forms.CharField(
                      max_length=150,
                      widget=forms.TextInput(attrs={
                          'class':'form-control',
                          'placeholder':'Recipient username'
                      })
                  )
    amount      = forms.DecimalField(
                      max_digits=12, decimal_places=2, min_value=0.01,
                      widget=forms.NumberInput(attrs={
                          'class':'form-control', 'placeholder':'Amount'
                      })
                  )
    description = forms.CharField(
                      required=False, max_length=255,
                      widget=forms.TextInput(attrs={
                          'class':'form-control',
                          'placeholder':'Description (optional)'
                      })
                  )

    def clean_recipient(self):
        username = self.cleaned_data['recipient']
        try:
            return get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            raise forms.ValidationError("No user with that username")
