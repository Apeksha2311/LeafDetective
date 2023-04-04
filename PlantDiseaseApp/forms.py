
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm

from django.contrib.auth.models import User

from django import forms
from .models import ImageModel


class RegisterForm(UserCreationForm):

    password1 = forms.CharField(label='Enter Your Password' , widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password here'}))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your confirm Password here'}))


    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'username' , 'email']

        labels = {
            'first_name':'Enter Your Name',
            'last_name':'Enter your Last Name',
            'username':'Enter your Username',
            'email':'Enter Your Email-ID'
        }

        widgets = {

            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})



        }

        

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Enter your Username',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Username..'}))

    password = forms.CharField(label='Enter Your Password' , widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password..'}))
    class Meta:
        model = User
        fields = ['username' , 'password']

class ImageForm(forms.ModelForm):

    class Meta:
        model = ImageModel
        fields = ['title','cat','image','desc']

        labels ={
            'title':'Enter title',
            'cat':'Select Image Category',
            'image':'Upload Image',
            'desc':'Enter Image description'
        }

        widgets = {
            'title':forms.TextInput(attrs={"class":'form-control'}),
            'cat':forms.Select(attrs={"class":'form-control'}),
            'image':forms.FileInput(attrs={"class":'form-control'}),
            'desc':forms.Textarea(attrs={"class":'form-control'})
        }