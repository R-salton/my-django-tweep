from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('profile_list/',views.profile_list, name="profile_list"),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('register/', views.register, name="register"),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('likes', views.Likes, name='likes')
   
]
