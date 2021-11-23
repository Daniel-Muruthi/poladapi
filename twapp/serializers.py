from rest_framework import serializers

from twapp.views import PostView
from .models import TwitterCreds, Profile, Post
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from allauth.account.adapter import get_adapter 

#User Serializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TwitterCredsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwitterCreds
        fields = ['atname', 'email', 'phone', 'password', 'url']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['email', 'phone', 'bio', 'gender', 'userpic']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id','content', 'created_at', 'tweet_at', 'sent']

    def get_initial(self):
        initial = super(PostView, self).get_initial()
        initial['user'] = User.objects.get(user_pk=self.kwargs['pk'])
        return initial



    def create(self,  validated_data):
        # serializer.save(user=self.request.user)
        x = Post.objects.create(**validated_data)
        x.save()
        return x
    def get_id(cls, user):
        token = super(PostSerializer, cls).get_token(user)

        # Add custom claims
        token['id'] = user.id
        return token


class LoginSerializer(TokenObtainPairSerializer):
    # email = serializers.EmailField(
    #         required=True,
    #         validators=[UniqueValidator(queryset=User.objects.all())]
    #         )
    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ('email','password',)
    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email', 'password', 'password2',  )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


    # def get_cleaned_data(self):
    #     return {
    #         'first_name': self.validated_data.get('first_name', ''),
    #         'last_name': self.validated_data.get('last_name', ''),
    #         'address': self.validated_data.get('address', ''),
    #         'user_type': self.validated_data.get('user_type', ''),
    #         'password1': self.validated_data.get('password1', ''),
    #         'email': self.validated_data.get('email', ''),
    #     }

    # def save(self, request):
    #     adapter = get_adapter()
    #     user = adapter.new_user(request)
    #     self.cleaned_data = self.get_cleaned_data()
    #     adapter.save_user(request, user, self)
    #     # setup_user_email(request, user, [])
    #     return user

    #     user.save()
    #     return user

    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
    
    #     user.first_name = validated_data['first_name']
    #     user.last_name  = validated_data['last_name']
    #     user.save()
    #     return user

    # @classmethod
    # def get_token(cls, user):
    #     token = super(RegisterSerializer, cls).get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     return token

