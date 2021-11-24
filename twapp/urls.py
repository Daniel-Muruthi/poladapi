from twapp import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('twittercreds', views.TwitterCredsView)
router.register('profile', views.ProfileView)
router.register('post', views.PostView)
router.register('apicreds', views.ApiCredsView)


urlpatterns = [
    path('profile/', views.MyProfile.as_view() , name="profile"),
    path('home/', views.MyTwitter.as_view() , name="home"),
    path('twitter/', views.MyTwitter.as_view(), name="tweety" ),
    path('api/', include(router.urls)),
]