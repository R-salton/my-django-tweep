from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from .views import UserRegistrationView,UserProfileView, UserFollowView, UserUnfollowView, UserFollowersView, UserFollowingView, ListTweepsView, ListProfilesView, UserTweepsView, LikeTweepView

from django.urls import re_path


from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import obtain_auth_token


schema_view = get_schema_view(
    openapi.Info(
        title="SaTweep API Documentation",
        default_version='v1',
        description="Documentation on How to use Satweep Social APIs to generate and Manipulate some Tweeps",
        terms_of_service="https://www.satweep.com/terms/",
        contact=openapi.Contact(email="nezasalton@gmail.com"),
        license=openapi.License(name="@salton 2023"),
    ),
    public=True,
    
      permission_classes=(permissions.AllowAny,),
    
)


urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'), # Done
    path('api/profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'), # Done
    path('api/profile/follow/', UserFollowView.as_view(), name='user-follow'),
    path('api/profile/unfollow/', UserUnfollowView.as_view(), name='user-unfollow'),
    path('api/profile/followers/', UserFollowersView.as_view(), name='user-followers'), # Done
    path('api/profile/following/', UserFollowingView.as_view(), name='user-following'), # Done
    path('api/tweeps/', ListTweepsView.as_view(), name='list-tweeps'), # Done
    path('api/profiles/', ListProfilesView.as_view(), name='list-profiles'), # Done
    path('api/user/<int:user_id>/tweeps/', UserTweepsView.as_view(), name='user-tweeps'), # Done
    path('api/tweeps/<int:tweep_id>/like/', LikeTweepView.as_view(), name='like-tweep'),
    
    path('api/token/', obtain_auth_token, name='token'),  # Add the token URL
    # ... your other API patterns ...
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # ...
]

    # Other URL patterns
