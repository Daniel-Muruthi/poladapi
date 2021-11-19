"""twoject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from twapp import views as twapp_views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

# router = routers.DefaultRouter()
# router.register('signup', twapp_views.T)
# router.register('profile', views.ProfileView)
# router.register('post', views.PostView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('twapp.urls')),
    path('signup/', twapp_views.signup, name="signup" ),
    path('signin/', auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path('auth/login/', twapp_views.LoginView.as_view(), name="signin"),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('auth/register/', twapp_views.RegisterView.as_view(), name='register'),
]
