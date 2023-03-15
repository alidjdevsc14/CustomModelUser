from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Contact, Seller, SellerAdditional, ProductInCart
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
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
            'query'
        ]


class RegistrationFormSeller(UserCreationForm):
    gst = forms.CharField(max_length=10)
    warehouse_location = forms.CharField(max_length=1000)

    class Meta:
        model = Seller
        fields = [
            'email',
            'name',
            'password1',
            'password2',
            'gst',
            'warehouse_location'
        ]


class RegistrationFormSeller2(forms.ModelForm):
    class Meta:
        model = SellerAdditional
        fields = [
            'gst',
            'warehouse_location'
        ]


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'name',
            'password1',
            'password2'
        ]


class CartForm(forms.ModelForm):
    class Meta:
        model = ProductInCart
        fields = [
            'quantity'
        ]
