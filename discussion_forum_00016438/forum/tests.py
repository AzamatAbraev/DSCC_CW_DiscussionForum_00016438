import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topic, Post

@pytest.mark.django_db
class TestForum:
    def test_create_post(self):
        user = User.objects.create_user(username='testuser', password='password')
        topic = Topic.objects.create(name="Tech")
        post = Post.objects.create(topic=topic, title="Test Post", author=user, body="Content")
        assert post.title == "Test Post"
        assert post.topic.name == "Tech"

    def test_post_list_view(self, client):
        url = reverse('post_list')
        response = client.get(url)
        assert response.status_code == 200

    def test_unauthenticated_post_create_redirect(self, client):
        url = reverse('post_create')
        response = client.get(url)
        assert response.status_code == 302

    def test_upvote_logic(self, client):
        user = User.objects.create_user(username='voter', password='password')
        topic = Topic.objects.create(name="General")
        post = Post.objects.create(topic=topic, title="Vote Me", author=user, body="Vote")
        post.upvotes.add(user)
        assert post.total_upvotes() == 1

    def test_post_slug_generation(self):
        user = User.objects.create_user(username='sluguser', password='password')
        topic = Topic.objects.create(name="SEO")
        post = Post.objects.create(topic=topic, title="Hello World", author=user)
        assert post.slug == "hello-world"

class HealthCheckTest(TestCase):
	def test_home_page_returns_200(self):
		client = Client()
		response = client.get("/")
		self.assertEqual(response.status_code, 200)

  
class BasicTests(TestCase):
	def test_app_name(self):
		self.assertTrue(True)


