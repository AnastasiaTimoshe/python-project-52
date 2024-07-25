from django.test import TestCase, Client
from task_manager.users.models import Users
from django.urls import reverse


class UsersTest(TestCase):

    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()

    def test_users_exist(self):
        self.assertEqual(Users.objects.count(), 5)

    def test_user_attributes(self):
        user2 = Users.objects.get(pk="3")
        self.assertEqual(user2.username, "tim2")
        self.assertEqual(user2.first_name, "tim")

    def test_user_create(self):
        url = reverse("user_create")
        user = {
            "first_name": "Anna",
            "last_name": "Tim",
            "username": "AnnaT",
            'password1': 'tim',
            'password2': 'tim',
        }
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, 302)
        test_user = Users.objects.last()
        assert test_user.first_name == "Anna"
        self.assertEqual(Users.objects.count(), 6)
        new_user = Users.objects.get(username="AnnaT")
        self.assertEqual(new_user.last_name, "Tim")

    def test_user_update(self):
        user1 = Users.objects.get(pk="2")
        url = reverse("user_update", args=[user1.pk])
        self.client.force_login(user1)
        update_user = {
            "first_name": user1.first_name,
            "last_name": user1.last_name,
            "username": "Tim1",
            'password1': user1.password,
            'password2': user1.password,
        }
        response = self.client.post(url, update_user)
        updated_user = Users.objects.get(pk=user1.pk)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        self.assertEqual(updated_user.username, "Tim1")

    def test_user_update_without_permission(self):
        user1 = Users.objects.get(pk="2")
        user2 = Users.objects.get(pk="3")
        url = reverse("user_update", args=[user2.pk])
        update_user = {
            "first_name": user1.first_name,
            "last_name": user1.last_name,
            "username": "Tim1",
            'password1': user1.password,
            'password2': user1.password,
        }
        self.client.force_login(user1)
        response = self.client.get(url, update_user)
        self.assertRedirects(response, reverse("users_list"))
        self.assertEqual(user1.username, "tim")

    def test_user_delete(self):
        self.assertEqual(Users.objects.count(), 5)
        user4 = Users.objects.get(pk="5")
        self.client.force_login(user4)
        url = reverse("user_delete", args=[user4.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 4)

    def test_delete_user_without_permission(self):
        self.assertEqual(Users.objects.count(), 5)
        user4 = Users.objects.get(pk="5")
        user5 = Users.objects.get(pk="2")
        self.client.force_login(user5)
        url = reverse("user_delete", args=[user4.pk])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 5)
