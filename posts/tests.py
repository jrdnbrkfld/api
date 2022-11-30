from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='Bob', password='Bobtest')

    def test_can_list_posts(self):
        Bob = User.objects.get(username='Bob')
        Post.objects.create(owner=Bob, title='The title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='Bob', password='Bobtest')
        response = self.client.post('/posts/', {'title': 'The title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        Bob = User.objects.create_user(username='Bob', password='Bobtest')
        Tony = User.objects.create_user(username='Tony', password='1234')
        Post.objects.create(
            owner=Bob, title='The title', content='Bobs content'
        )
        Post.objects.create(
            owner=Tony, title='Another title', content='Tonys content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'The title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/9000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_their_post(self):
        self.client.login(username='Bob', password='Bobtest')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_anothers_post(self):
        self.client.login(username='Bob', password='Bobtest')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
