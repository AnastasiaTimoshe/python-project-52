from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import Users
from django.contrib.messages import get_messages


class UsersTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()

    def test_users_exist(self):
        self.assertEqual(Users.objects.count(), 5)

    def test_user_attributes(self):
        user3 = Users.objects.get(pk=3)
        self.assertEqual(user3.username, "executor")
        self.assertEqual(user3.first_name, "")

    def test_create_user(self):
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

    def test_update_user(self):
        user2 = Users.objects.get(pk=2)
        self.client.force_login(user2)
        url = reverse("user_update", args=[user2.pk])

        update_data = {
            "first_name": "UpdatedName",
            "last_name": "UpdatedLastName",
            "username": "Emi2015",
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        response = self.client.post(url, update_data, follow=True)

        self.assertRedirects(response, reverse("users_list"))
        updated_user = Users.objects.get(pk=user2.pk)
        self.assertEqual(updated_user.username, "Emi2015")

    def test_update_user_without_permission(self):
        user2 = Users.objects.get(pk=2)
        user3 = Users.objects.get(pk=3)
        self.client.force_login(user2)
        url = reverse("user_update", args=[user3.pk])

        update_data = {
            "first_name": "UpdatedName",
            "last_name": "UpdatedLastName",
            "username": "Emi2015",
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        response = self.client.post(url, update_data, follow=True)

        self.assertRedirects(response, reverse("users_list"))
        user3.refresh_from_db()
        self.assertEqual(user3.username, "executor")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn("У вас нет прав для изменения", str(messages[0]))

    def test_delete_user(self):
        self.client.force_login(Users.objects.get(pk=1))
        self.assertEqual(Users.objects.count(), 5)

        user_to_delete = Users.objects.get(pk=5)
        url = reverse("user_delete", args=[user_to_delete.pk])
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 5)

    def test_delete_user_without_permission(self):
        self.assertEqual(Users.objects.count(), 5)

        user_to_delete = Users.objects.get(pk=3)
        user_without_permission = Users.objects.get(pk=2)
        self.client.force_login(user_without_permission)
        url = reverse("user_delete", args=[user_to_delete.pk])
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 5)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn("У вас нет прав для удаления другого пользователя.", str(messages[0]))
