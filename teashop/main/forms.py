from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ProductReview, UserAddressBook


class SignupForm(UserCreationForm):
    # full_name = forms.CharField(max_length=50, required=True, label='ФИО')
    # mobile = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'type': 'number'}), label='Телефон')
    # address = forms.CharField(max_length=50, required=True, label='Адрес')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class ReviewAdd(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('review_text', 'review_rating')

class AddressBookForm(forms.ModelForm):
    class Meta:
        model = UserAddressBook
        fields=('address', 'mobile', 'status')

class ProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email','username')