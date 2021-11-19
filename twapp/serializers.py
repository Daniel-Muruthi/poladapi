from rest_framework import serializers
from .models import TwitterCreds, Profile, Post
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class TwitterCredsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwitterCreds
        fields = ['atname', 'email', 'phone', 'password', 'url']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['email', 'phone', 'bio', 'gender', 'userpic']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'created_at', 'tweet_at', 'sent']


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
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
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )

        
    #     user.set_password(validated_data['password'])
    #     user.save()

    #     return user

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
    
        user.first_name = validated_data['first_name']
        user.last_name  = validated_data['last_name']
        user.save()
        return user

    # @classmethod
    # def get_token(cls, user):
    #     token = super(RegisterSerializer, cls).get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     return token

