from django.contrib import admin
from .models import Profile, TwitterCreds, Post
# Register your models here.
admin.site.register(Profile)
admin.site.register(TwitterCreds)
admin.site.register(Post)