from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ApiCredsModel, Post
from .views import ApiCredsView

# @receiver(post_save, sender=User)
# def create_apicredsmodel(sender, instance, created, **kwargs):
#     if created:
#         ApiCredsModel.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_apicredsmodel(sender, instance, **kwargs):
#     instance.apicredsmodel.save()

# def get_initial(self):
#     initial = super(ApiCredsView, self).get_initial()
#     initial['user'] = User.objects.get(user_pk=self.kwargs['pk'])
#     return initial

# @receiver(post_save, sender=User)
# def create_postmodel(sender, instance, created, **kwargs):
#     if created:
#         Post.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_postmodel(sender, instance, **kwargs):
#     instance.post.save()