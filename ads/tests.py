
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Ad

class AdAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com', password='password123'
        )
        self.other_user = get_user_model().objects.create_user(
            email='other@example.com', password='password123'
        )
        self.ad = Ad.objects.create(
            user=self.user,
            title="Test Ad",
            description="Test Ad Description"
        )
        self.list_url = reverse('ad-list')
        self.create_url = reverse('ad-create')
        self.detail_url = reverse('ad-detail', args=[self.ad.id])
        self.update_url = reverse('ad-update', args=[self.ad.id])
        self.delete_url = reverse('ad-delete', args=[self.ad.id])

    def test_list_ads(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Ad.objects.count())

    def test_create_ad_authenticated(self):
        self.client.login(email='user@example.com', password='password123')
        data = {'title': 'New Ad', 'description': 'New Ad Description'}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 2)
        self.assertEqual(Ad.objects.last().user, self.user)

    def test_create_ad_unauthenticated(self):
        data = {'title': 'New Ad', 'description': 'New Ad Description'}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_ad(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.ad.id)

    def test_update_ad_owner(self):
        self.client.login(email='user@example.com', password='password123')
        data = {'title': 'Updated Title', 'description': 'Updated Description'}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Title')

    def test_update_ad_not_owner(self):
        self.client.login(email='other@example.com', password='password123')
        data = {'title': 'Updated Title', 'description': 'Updated Description'}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ad_owner(self):
        self.client.login(email='user@example.com', password='password123')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 0)

    def test_delete_ad_not_owner(self):
        self.client.login(email='other@example.com', password='password123')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Ad.objects.count(), 1)
