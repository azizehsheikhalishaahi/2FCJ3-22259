from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ads.models import Ad
from .models import Comment

User = get_user_model()

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.ad = Ad.objects.create(title='Test Ad', description='Test Description', user=self.user) 
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_create_comment(self):
        url = f'/comments/ads/{self.ad.id}/add/'
        data = {
            'text': 'Great ad!',
            'ad': self.ad.id
        }
        response = self.client.post(url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().text, 'Great ad!')

    def test_create_comment_twice(self):
        url = f'/comments/ads/{self.ad.id}/add/'
        self.client.post(url, {'text': 'First comment'})
        response = self.client.post(url, {'text': 'Second comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_comments(self):
        Comment.objects.create(ad=self.ad, user=self.user, text='Test comment')
        url = f'/comments/ads/{self.ad.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
