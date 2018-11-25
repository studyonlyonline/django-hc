from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, User, Dealer
from django import forms

class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Display Name"
        self.fields['email'].label = "Email Address"

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'contact_no',
            'delivery_address',
            'apply_for_dealership'
        ]

class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = [
            'gstin',
            'company_name'
        ]
