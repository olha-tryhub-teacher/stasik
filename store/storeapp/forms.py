from django import forms
from .models import Order_product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ClientCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Order_product
        fields = ['amount']