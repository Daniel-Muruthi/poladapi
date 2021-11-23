from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import DEFERRED
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
# Create your models here.
User = settings.AUTH_USER_MODEL



GENDER_CHOICES = (
   ('M', 'Male'),
   ('F', 'Female'),
   ('O', 'Other')
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.CharField(null=True, max_length=255)
    phone = PhoneNumberField(null=True)
    bio = models.CharField(blank=True,max_length=255)
    userpic = CloudinaryField('image')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=11,  default='Male')

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)


    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    post_save.connect(save_user_profile, sender=User)


    class Meta:
        ordering = ('-user',)


class TwitterCreds(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    atname = models.CharField(null=True, max_length=255)
    email = models.CharField(null=True, max_length=255)
    phone = PhoneNumberField(null=True)
    password = models.CharField(null=True, max_length=255)

    def __str__(self):
        return str(self.user.username)

    
    @classmethod
    def myphone(cls, phone):
        a = cls.objects.filter(phone=phone)
        return a
    @classmethod
    def mypassword(cls, password):
        b = cls.objects.filter(password=password)
        return b

    def create_user_twittercreds(sender, instance, created, **kwargs):
        if created:
            TwitterCreds.objects.create(user=instance)
    post_save.connect(create_user_twittercreds, sender=User)


    def save_user_twittercreds(sender, instance, **kwargs):
        instance.twittercreds.save()
    post_save.connect(save_user_twittercreds, sender=User)

    
    # def getprojectbyid(request):
    #     current_user = User.is_authenticated()
    #     return current_user.id



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    tweet_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    sent = models.BooleanField(default=False)


    
    def __str__(self):
        return str(self.user)

    # def get_object(self,**kwargs):
        
    #     a = Post.objects.get_or_create(id=self.id)
    #     for obj in TwitterCreds.objects.all():
    #         if obj.id == a:
    #             return a

    def get_object(self):
        x=self
        return x
    def get_absolute_url(self):
        return self.content

    def save(self, *args, **kwargs):
        return super(Post, self).save(*args, **kwargs)


#######################################################

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:Token.objects.create(user=instance)
