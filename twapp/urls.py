from twapp import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('twittercreds', views.TwitterCredsView)
router.register('profile', views.ProfileView)
router.register('post', views.PostView)
urlpatterns = [
    path('', views.index, name="index"),
    path ('profile/update/', views.EditProfile, name="update"),
    path('profile/', views.MyProfile.as_view() , name="profile"),
    path('polad/tweet/', views.automate, name="automate"),
    path('home/', views.MyTwitter.as_view() , name="home"),
    path('twitter/update/', views.EditTwitter, name="edittwitter"),
    path('twitter/', views.MyTwitter.as_view(), name="tweety" ),
    path('tweet/', views.newpost, name='newpost'),
    path('api/', include(router.urls)),
]