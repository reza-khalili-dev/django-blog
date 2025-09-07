from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post
from .forms import PostForm


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            author=self.user,
            status="published",
        )

    def test_post_content(self):
        self.assertEqual(self.post.title, "Test Post")

    def test_post_str(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_post_author(self):
        self.assertEqual(self.post.author.username, "testuser")

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/post/test-post/")

class PostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            author=self.user,
            status="published",
        )

    def test_post_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_post_detail_view(self):
        response = self.client.get(self.post.get_absolute_url())
        no_response = self.client.get("/post/not-found/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/post_detail.html")

    def test_post_create_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("post_new"))
        self.assertNotEqual(response.status_code, 200)  # چون لاگین نیستیم

    def test_post_create_view_logged_in(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "Another Test Post",
                "slug": "another-test-post",
                "content": "New post content",
                "status": "published",
            },
        )
        self.assertEqual(response.status_code, 302) 

class PostFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create_user(username="testuser", password="12345")
        form_data = {
            "title": "Valid Title",
            "slug": "valid-title",
            "content": "Valid content",
            "status": "published",
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "title": "Hi", 
            "slug": "invalid-slug",
            "content": "Some content",
            "status": "draft",
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

class UrlsTest(TestCase):
    def test_home_url(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
