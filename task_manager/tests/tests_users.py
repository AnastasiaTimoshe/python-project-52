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
        user3 = Users.objects.get(pk=3)
        self.assertEqual(user3.username, "executor")
        self.assertEqual(user3.first_name, "")

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
        user2 = Users.objects.get(pk=2)
        self.client.force_login(user2)
        url = reverse("user_update", args=[user2.pk])

        update_data = {
            "first_name": user2.first_name,
            "last_name": user2.last_name,
            "username": "Emi2015",
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        response = self.client.post(url, update_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))

        updated_user = Users.objects.get(pk=user2.pk)
        self.assertEqual(updated_user.username, "Emi2015")

    def test_user_update_without_permission(self):
        user2 = Users.objects.get(pk=2)
        user3 = Users.objects.get(pk=3)
        self.client.force_login(user2)
        url = reverse("user_update", args=[user3.pk])

        update_data = {
            "first_name": user3.first_name,
            "last_name": user3.last_name,
            "username": "Emi2015",
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        response = self.client.post(url, update_data)

        self.assertRedirects(response, reverse("users_list"))

        user3.refresh_from_db()
        self.assertEqual(user3.username, "executor")

    def test_user_delete(self):
        self.assertEqual(Users.objects.count(), 5)
        user4 = Users.objects.get(pk=5)
        self.client.force_login(user4)
        url = reverse("user_delete", args=[user4.pk])
        response = self.client.post(url)

        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 4)

    def test_delete_user_without_permission(self):
        self.assertEqual(Users.objects.count(), 5)

        user4 = Users.objects.get(pk=5)
        user2 = Users.objects.get(pk=2)
        self.client.force_login(user2)
        url = reverse("user_delete", args=[user4.pk])
        response = self.client.post(url)

        self.assertRedirects(response, reverse('users_list'))

        self.assertEqual(Users.objects.count(), 5)

        messages = list(response.wsgi_request._messages)
        expected_error_message = "У вас нет прав для удаления другого пользователя."
        self.assertTrue(
            any(expected_error_message in str(m) for m in messages),
            "Сообщение об ошибке не найдено"
        )
