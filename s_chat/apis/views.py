from django.shortcuts import render
# from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .serializers import UserRegistrationSerializer,TweepSerializer
from social.models import Profile,Tweep
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.throttling import UserRateThrottle
from django_ratelimit.decorators import ratelimit
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# Create your views here.

def home(request):
    return render(request,'home.html',{})



class UserRegistrationView(APIView):
    authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        serializer_class = UserRegistrationSerializer
        kwargs['context'] = self.get_serializer_context()
        kwargs['fields'] = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        return serializer_class(*args, **kwargs)



class UserProfileView(APIView):
    
    authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def get(self, request, user_id):  # Accept user_id parameter
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class UserFollowView(APIView):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [permissions.IsAuthenticated]  
    throttle_classes = [UserRateThrottle]
    
    def post(self, request):
        user_to_follow_id = request.data.get('user_id')

        if user_to_follow_id:
            try:
                user_to_follow_profile = Profile.objects.get(id=user_to_follow_id)
                user_profile = Profile.objects.get(user=request.user)
                user_profile.follows.add(user_to_follow_profile)
                return Response({'message': 'User followed successfully'}, status=status.HTTP_201_CREATED)
            except Profile.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Missing user_id in request'}, status=status.HTTP_400_BAD_REQUEST)

class UserUnfollowView(APIView):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [permissions.IsAuthenticated]  
    throttle_classes = [UserRateThrottle]
    
    def post(self, request):
        user_to_unfollow_id = request.data.get('user_id')

        if user_to_unfollow_id:
            try:
                user_to_unfollow_profile = Profile.objects.get(id=user_to_unfollow_id)
                user_profile = Profile.objects.get(user=request.user)
                user_profile.follows.remove(user_to_unfollow_profile)
                return Response({'message': 'User unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)
            except Profile.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Missing user_id in request'}, status=status.HTTP_400_BAD_REQUEST)

# Display all Your Followers

class UserFollowersView(APIView):
   
    authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        followers = profile.followed_by.all()
        serializer = ProfileSerializer(followers, many=True)
        return Response(serializer.data)


# Display all user That You follow

class UserFollowingView(APIView):
    
    authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        following = profile.follows.all()
        serializer = ProfileSerializer(following, many=True)
        return Response(serializer.data)


# list All Tweeps

class ListTweepsView(APIView):
    authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        tweeps = Tweep.objects.all()
        serializer = TweepSerializer(tweeps, many=True)
        
        return Response(serializer.data)
    
 # Dislay all profiles    
    
class ListProfilesView(APIView):
    authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
# Display  tweeps for specific user using User_id

class UserTweepsView(APIView):
    authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def get(self, request, user_id):
        tweeps = Tweep.objects.filter(user_id=user_id)
        serializer = TweepSerializer(tweeps, many=True)
        return Response(serializer.data)
    
    
class LikeTweepView(APIView):
    authentication_classes = [TokenAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle] # Require authentication

    def post(self, request, tweep_id):
        try:
            tweep = Tweep.objects.get(id=tweep_id)
        except Tweep.DoesNotExist:
            return Response({'message': 'Tweep not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in tweep.likes.all():
            return Response({'message': 'You have already liked this tweep'}, status=status.HTTP_400_BAD_REQUEST)

        tweep.likes.add(user)
        return Response({'message': 'Tweep liked successfully'}, status=status.HTTP_200_OK)