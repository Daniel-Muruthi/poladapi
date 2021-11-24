from django.contrib import admin
from .models import Profile, TwitterCreds, Post, TwitterSchedulerModel, ApiCredsModel
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
admin.site.register(Profile)
admin.site.register(TwitterCreds)
admin.site.register(Post)
admin.site.register(ApiCredsModel)
@admin.register(TwitterSchedulerModel)
class TwitterSchedulerAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'tweet_at', 'created_at', 'sent')
    search_fields = ('tweet', 'tweet_at', 'created_at')