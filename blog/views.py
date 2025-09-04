from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Post

# Create your views here.


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class ProfileView(LoginRequiredMixin,ListView):
    form = Post
    template_name = 'profile.html'
    context_object_name = 'posts'
    paginate_by = 10 

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user ).order_by('-created_at')
    