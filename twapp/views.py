from django.http.response import HttpResponseRedirect
import tweepy
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from decouple import config 
from selenium import webdriver
from django.contrib.auth.decorators import login_required
from .forms import PostForm, SignUpForm, ProfileUpdateForm, TwitterCredsForm
from django.contrib import messages
from django.views.generic import DetailView, FormView,UpdateView, CreateView, DeleteView, TemplateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from twapp.models import Profile, TwitterCreds, Post
import psycopg2
import re
import string
#######################################################
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from rest_framework import serializers, viewsets
from .serializers import PostSerializer, ProfileSerializer, TwitterCredsSerializer, LoginSerializer, RegisterSerializer


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
########################################################
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

# Create your views here.
#####################login###################
class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

############################################

#####################login###################
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

############################################

###############twitter creds#######################
# @method_decorator(csrf_exempt, name='creds')
class TwitterCredsView(viewsets.ModelViewSet):
    queryset = TwitterCreds.objects.all()
    serializer_class = TwitterCredsSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TwitterCredsView, self).dispatch(request, *args, **kwargs)
#######################################################

###############twitter creds#######################
# @method_decorator(csrf_exempt, name='prof')
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)
#######################################################

###############twitter creds#######################
# @method_decorator(csrf_exempt, name='posts')
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PostView, self).dispatch(request, *args, **kwargs)

#######################################################

def index(request):
    

    return render(request, 'index.html')

def login(request):
    return render(request, 'auth/login.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form':form})

class MyProfile(DetailView):
    model = Profile
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user.profile


@login_required
def EditProfile(request):
    profileform = ProfileUpdateForm(instance=request.user.profile)
    pform = None
    if request.method == 'POST':
        profileform=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if profileform.is_valid():
            pform=profileform.save(commit=False)
            pform.user = request.user
            pform.profile = profileform
            pform.save()


            return redirect('profile')

        else:
            profileform = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user': request.user,
        'profileform': profileform, 
        'pform':pform,
    }
    return render(request, 'profileedit.html', context)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    fields = ['userpic', 'houselocation','user', 'email', 'phonenumber', 'bio', 'gender']
    template_name = 'profileedit.html'
    # form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Your Account Settings were updated successfully!')
        return reverse('profile')


############################################################

def automate(request):

    tform = TwitterCredsForm(instance=request.user.twittercreds)
    form = None
    if request.method == "POST":
        tform = TwitterCredsForm(request.POST, request.FILES,)
        if tform.is_valid():
            form=TwitterCredsForm.save(commit=False)
            form.user = request.user
            form.twittercreds = tform
            form.save()
            
            return redirect('home')

        else:
            tform = TwitterCredsForm(instance=request.user.twittercreds)

    context = {
        'user': request.user,
        'form': tform, 
    }
    return render(request, 'home.html', context)


@login_required
def userhome(request):

    return render(request, 'home.html', {'form':TwitterCredsForm()})

########updating twitter credentials#############
@login_required
def EditTwitter(request):
    twitterform = TwitterCredsForm(instance=request.user.twittercreds)
    tform = None
    if request.method == 'POST':
        twitterform=TwitterCredsForm(request.POST, request.FILES, instance=request.user.twittercreds)

        if twitterform.is_valid():
            tform=twitterform.save(commit=False)
            tform.user = request.user
            tform.twittercreds = twitterform
            tform.save()


            return redirect('twittercreds')

        else:
            twitterform = TwitterCredsForm(instance=request.user.twittercreds)

    context = {
        'user': request.user,
        'twitterform': twitterform, 
        'tform':tform,
    }
    return render(request, 'home.html', context)

##################################################

########Twitter Credentials Display##############

class MyTwitter(DetailView):
    model = TwitterCreds
    template_name = 'twittercreds.html'

    def get_object(self):
        return self.request.user.twittercreds

################################################

#########create Post##########################

def newpost(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.twittercreds = form
            post.save()
            messages.success(request, 'You Have succesfully Tweeted')
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'userhome.html', {"form": form})

##############################################

