from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields= "__all__"
        exclude = ['host', 'participants']
        
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'avatar', 'username', 'email', 'bio']
        
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

# class RegisterForm(UserCreationForm):
#     class Meta:
#         model=User
#         fields = ['username','email','password1','password2'] 
   
