from django import forms
from django.forms import ModelForm, Textarea,TextInput, FileInput,Select, DateInput, NumberInput
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)

class UserChange(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','profile_photo',)
