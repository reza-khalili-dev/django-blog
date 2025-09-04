from django.urls import path
from . import views

urlpatterns = [
    
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('',views.PostListView.as_view(), name='home'), 
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    

    
]
