from django.forms import ModelForm
from .models import Product, Photo, Cart, Wish, Orders, OrderDatails
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ImageField, ClearableFileInput


class RegisterForm ( UserCreationForm ):
    email = forms.EmailField ( max_length=25, help_text='Required' )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class MYPasswordChangeForm ( PasswordChangeForm ):
    def __init__(self, *args, **kwargs):
        super ().__init__ ( *args, **kwargs )
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs = {'class': 'form-control'}


class ProductForm ( ModelForm ):
    class Meta:
        model = Product
        fields = ["name", "price", "count", "description"]


class ProductPhotoForm ( forms.ModelForm ):
    photo_url = ImageField ( widget=ClearableFileInput ( attrs={"multiple": True, "accept": "image/*"} ) )

    class Meta:
        model = Photo
        fields = ["photo_url"]


class CartForm ( ModelForm ):
    class Meta:
        model = Cart
        fields = ["user", "count", "product"]


class WishForm ( ModelForm ):
    class Meta:
        model = Wish
        fields = ["user", "product", ]


class OrdersForm ( ModelForm ):
    class Meta:
        model = Orders
        fields = ['total', 'data']


class OrderDatailsForm ( ModelForm ):
    class Meta:
        model = OrderDatails
        fields = ['count', 'feedback']
