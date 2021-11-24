from rest_framework import serializers
from .models import TwitterCreds, Profile, Post, ApiCredsModel
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
        # extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class TwitterCredsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwitterCreds
        fields = ['atname', 'email', 'phone', 'password', 'url']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['email', 'phone', 'bio', 'gender', 'userpic']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    # created_at = serializers.DateTimeField(read_only=True)
    # user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = ['id','content', 'created_at', 'tweet_at', 'sent']
        read_only_fields = ('user', 'created_at',)



    def create(self,  validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        x= super().create(validated_data)
        x.save()
        return x


    def get_id(cls, user):
        token = super(PostSerializer, cls).get_token(user)

        # Add custom claims
        token['id'] = user.id
        return token

    # def create(self, validated_data):
    #     user_data = self.context['request']
    #     user_instance = User.objects.create(
    #         username=user_data['username'])
    #     user_instance.save()
        
    #     post_instance = Post.objects.create(
    #         **validated_data, user=user_instance)
    #     post_instance.save()
    #     return post_instance

class LoginSerializer(TokenObtainPairSerializer):

    class Meta:
        model = User
        fields = ('username','password',)
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


 

class ApiCredsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApiCredsModel
        fields = ['id', 'consumer_key', 'consumer_secret', 'access_token', 'token_secret', 'url']
        read_only_fields = ('user',)


    def create(self,  validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)