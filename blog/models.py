from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    title  = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    cntent= models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
