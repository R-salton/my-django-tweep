from django.contrib.auth.models import User
from rest_framework import serializers
from social.models import Profile, Tweep
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from django_ratelimit.decorators import ratelimit
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.views import get_schema_view



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email' ,'password']
        extra_kwargs = {'password': {'write_only': True}}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'follows','followed_by']
        
        


class TweepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweep
        fields = '__all__'


class Tokeverification(serializers.ModelSerializer):
    token = serializers.CharField(max_length= 555)
    class Meta:
        model = User