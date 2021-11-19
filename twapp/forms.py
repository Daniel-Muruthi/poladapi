from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Profile, TwitterCreds





class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}))


    class Meta:
        model = User
        fields =("username", "email", "password1", "password2",)

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def passwordcheck(self):
        password1 = self.cleaned_data.get("password1")
        password2= self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mistmatch'],
                code='password_mismatch',
            )
        return password2



class ProfileUpdateForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ['userpic','user', 'email', 'phone', 'bio', 'gender']


class TwitterCredsForm(forms.ModelForm):

    class Meta:
        model = TwitterCreds
        fields = ['email','phone','password', 'atname']

class PostForm(forms.ModelForm): 
    class Meta:
        model=Post
        fields = ['content']