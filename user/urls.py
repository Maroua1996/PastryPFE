from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),  
    path('change_profile_picture/', change_profile_picture, name='change_profile_picture'),
    path('user_information_view/<str:username>/', user_information_view, name='user_information_view'),
    path('follow/<int:user_id>/', follow_or_not, name='follow'),
    path('notifications/', user_notifications, name='notifications'),
    path('mute_or_not/<int:user_id>/', mute_or_not, name='mute_or_not'),
    path('delete_account/', delete_account, name='delete_account'),
   
  
    
]