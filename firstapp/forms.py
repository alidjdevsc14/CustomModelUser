from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Contact
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ContactUsForm(forms.ModelForm):
    # email = forms.EmailField(required=True)
    # name = forms.CharField(max_length=100, required=True)
    # phone = forms.CharField(max_length=10, required=True)
    # query = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'phone',
            'query',
        ]
