from django.test import TestCase, Client
from task_manager.users.models import Users
from django.urls import reverse
from django.contrib.messages import get_messages


class UsersTest(TestCase):

    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()

    def test_users_exist(self):
        self.assertEqual(Users.objects.count(), 5)

    def test_user_attributes(self):
        user = Users.objects.get(pk=3)
        self.assertEqual(user.username, "executor")
        self.assertEqual(user.first_name, "")

    def test_user_create(self):
        url = reverse("user_create")
        user_data = {
            "first_name": "Mia",
            "last_name": "Petrova",
            "username": "Mia2013",
            'password1': 'mia',
            'password2': 'mia',
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Users.objects.count(), 6)
        test_user = Users.objects.last()
        self.assertEqual(test_user.first_name, "Mia")
        self.assertEqual(test_user.username, "Mia2013")
        self.assertEqual(test_user.last_name, "Petrova")

    def test_user_update(self):
        user = Users.objects.get(pk=2)
        self.client.force_login(user)
        url = reverse("user_update", args=[user.pk])

        update_data = {
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "username": "Emi2015",
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        response = self.client.post(url, update_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))

        updated_user = Users.objects.get(pk=user.pk)
        self.assertEqual(updated_user.username, "Emi2015")

    def test_user_update_without_permission(self):
        user_with_permission = Users.objects.get(pk=2)
        user_to_update = Users.objects.get(pk=3)
        self.client.force_login(user_with_permission)
        url = reverse("user_update", args=[user_to_update.pk])

        update_data = {
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "username": "Emi2015",
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        response = self.client.post(url, update_data)

        self.assertRedirects(response, reverse("users_list"))

        user_to_update.refresh_from_db()
        self.assertEqual(user_to_update.username, "executor")

    def test_user_delete(self):
        self.client.force_login(Users.objects.get(pk=1))
        self.assertEqual(Users.objects.count(), 5)

        user_to_delete = Users.objects.get(pk=5)
        url = reverse("user_delete", args=[user_to_delete.pk])
        response = self.client.post(url)

        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 5)

    def test_delete_user_without_permission(self):
        self.assertEqual(Users.objects.count(), 5)

        user_to_delete = Users.objects.get(pk=5)
        user_without_permission = Users.objects.get(pk=2)
        self.client.force_login(user_without_permission)
        url = reverse("user_delete", args=[user_to_delete.pk])

        response = self.client.post(url)

        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 5)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(str(message) == "У вас нет прав для удаления другого пользователя."
                for message in messages))
