from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Ad

User = get_user_model()

class AdTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(email='testuser@example.com', password='testpassword')
        self.ad = Ad.objects.create(user=self.user, title='Test Ad', description='Test Description')

    def test_create_ad(self):
        url = '/ads/'  # Endpoint for creating an ad
        data = {'title': 'New Ad', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 2)  # Assuming there's already one ad created in setUp
        self.assertEqual(Ad.objects.latest('id').title, 'New Ad')

    def test_edit_ad(self):
        url = f'/ads/{self.ad.id}/'
        data = {'title': 'Updated Title', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Title')

    def test_delete_ad(self):
        url = f'/ads/{self.ad.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())
