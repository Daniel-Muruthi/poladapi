from django.contrib import admin
from .models import Profile, TwitterCreds, Post
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
admin.site.register(Profile)
admin.site.register(TwitterCreds)
admin.site.register(Post)