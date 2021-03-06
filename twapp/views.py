from django.http.response import HttpResponseRedirect
import tweepy
from django.core.exceptions import ValidationError
from rest_framework.response import Response
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
from twapp.models import Profile, TwitterCreds, Post, ApiCredsModel, TwitterSchedulerModel
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
from .serializers import PostSerializer, ProfileSerializer, TwitterCredsSerializer, LoginSerializer, RegisterSerializer, UserSerializer, ApiCredsSerializer
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
########################################################
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import mixins, viewsets
from .permissions import IsAdminOrIsSelf
from rest_framework.decorators import action
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login as auth_login

# Create your views here.
#####################login###################

class LoginView(KnoxLoginView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        auth_login(request, user)
        return super(LoginView, self).post(request, format=None)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)
    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
############################################

###################userview####################
class UserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
############################################3#

#####################login###################


class RegisterView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        # "token": AuthToken.objects.create(user)[1]
        "token": Token.objects.get(user=user).key
        })

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
    permission_classes = (permissions.IsAuthenticated,)
    queryset = TwitterCreds.objects.all()
    serializer_class = TwitterCredsSerializer


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TwitterCredsView, self).dispatch(request, *args, **kwargs)
#######################################################

###############twitter creds#######################
# @method_decorator(csrf_exempt, name='prof')
class ProfileView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)
#######################################################

###############twitter creds#######################
# @method_decorator(csrf_exempt, name='posts')
class PostView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_initial(self):
        initial = super(PostView, self).get_initial()
        initial['user'] = User.objects.get(user_pk=self.kwargs['pk'])
        return initial

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PostView, self).dispatch(request, *args, **kwargs)
    # def create(self, request,  *args, **kwargs ):
    #     # serializer.save(user=self.request.user)
    #     post_data = request.data
    #     new_user_id = User.objects.create(id=post_data["user_id"][0])
    #     new_user_id.save()
    #     x = Post.objects.create(content=post_data["content"], created_at=post_data["created_at"], tweet_at=post_data["tweet_at"], sent=post_data["sent"],user_id=new_user_id)
    #     x.save()
    #     serializer = PostSerializer(x)
    #     return Response(serializer.data)
######################################################


class MyProfile(DetailView):
    model = Profile
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user.profile





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

########updating twitter credentials#############


##################################################

########Twitter Credentials Display##############

class MyTwitter(DetailView):
    model = TwitterCreds
    template_name = 'twittercreds.html'

    def get_object(self):
        return self.request.user.twittercreds

################################################

# @api_view(["GET"])
# @authentication_classes([SessionAuthentication,BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def login_user(request):

#         data = {}
#         reqBody = json.loads(request.body)
#         email1 = reqBody['email']
#         print(email1)
#         password = reqBody['password']
#         try:

#             Account = User.objects.get(email=email1)
#         except BaseException as e:
#             raise ValidationError({"400": f'{str(e)}'})

#         token = Token.objects.get_or_create(user=Account)[0].key
#         print(token)
#         if not check_password(password, Account.password):
#             raise ValidationError({"message": "Incorrect Login credentials"})

#         if Account:
#             if Account.is_active:
#                 print(request.user)
#                 login(request, Account)
#                 data["message"] = "user logged in"
#                 data["email_address"] = Account.email

#                 Res = {"data": data, "token": token}

#                 return Response(Res)

#             else:
#                 raise ValidationError({"400": f'Account not active'})

#         else:
#             raise ValidationError({"400": f'Account doesnt exist'})

class ApiCredsView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = ApiCredsModel.objects.all()
    serializer_class = ApiCredsSerializer

    def get_initial(self):
        initial = super(ApiCredsView, self).get_initial()
        initial['user'] = User.objects.get(user_pk=self.kwargs['pk'])
        return initial

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ApiCredsView, self).dispatch(request, *args, **kwargs)