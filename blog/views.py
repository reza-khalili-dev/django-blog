from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
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

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return (Post.objects.filter(status="published").select_related("author").order_by("-created_at"))

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        base_qs = Post.objects.select_related('author')
        if self.request.user.is_authenticated:
            return base_qs.filter(Q(status = 'published') | Q(author = self.request.user))
        return base_qs.filter(status = 'published')


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'slug', 'content', 'status']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

