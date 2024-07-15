from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserTests(TestCase):

    def test_create_user(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_update_user(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('user_update', args=[user.pk]), {
            'username': 'updateduser',
            'email': 'newemail@example.com',
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'newemail@example.com')

    def test_delete_user(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('user_delete', args=[user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())
