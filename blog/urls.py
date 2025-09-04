from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('',views.ProfileView.as_view(), name='home'), #just for now. after make a posts list, i change it 
    
]
