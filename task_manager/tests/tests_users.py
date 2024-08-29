from django.test import TestCase, Client
from task_manager.users.models import Users
from django.urls import reverse


class UsersTest(TestCase):

    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()

    def test_users_exist(self):
        # Проверяем количество пользователей, загруженных из фикстуры
        self.assertEqual(Users.objects.count(), 5)

    def test_user_attributes(self):
        # Проверяем, что пользователь с pk=3 имеет правильные атрибуты
        user3 = Users.objects.get(pk=3)
        self.assertEqual(user3.username, "executor")
        self.assertEqual(user3.first_name, "")

    def test_user_create(self):
        url = reverse("user_create")
        user = {
            "first_name": "Mia",
            "last_name": "Lukovic",
            "username": "Mia2013",
            'password1': 'mia',
            'password2': 'mia',
        }
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, 302)
        test_user = Users.objects.last()
        assert test_user.first_name == "Mia"
        self.assertEqual(Users.objects.count(), 6)
        new_user = Users.objects.get(username="Mia2013")
        self.assertEqual(new_user.last_name, "Lukovic")

    def test_user_update(self):
        # Обновляем пользователя с pk=2 и проверяем изменения
        user2 = Users.objects.get(pk=2)
        url = reverse("user_update", args=[user2.pk])
        self.client.force_login(user2)
        # Убедитесь, что пароль совпадает
        update_user = {
            "first_name": user2.first_name,
            "last_name": user2.last_name,
            "username": "Emi2015",
            'password1': 'securepassword',  # Убедитесь, что используется корректный пароль
            'password2': 'securepassword',  # Пароли должны совпадать
        }
        response = self.client.post(url, update_user)

        # Добавьте отладочный вывод ошибок формы
        if response.status_code == 200:
            print(response.context['form'].errors)

        updated_user = Users.objects.get(pk=user2.pk)
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление
        self.assertRedirects(response, reverse("users_list"))
        self.assertEqual(updated_user.username, "Emi2015")

    def test_user_update_without_permission(self):
        # Проверяем, что пользователь не может обновить другого пользователя без разрешения
        user2 = Users.objects.get(pk=2)
        user3 = Users.objects.get(pk=3)
        url = reverse("user_update", args=[user3.pk])
        update_user = {
            "first_name": user2.first_name,
            "last_name": user2.last_name,
            "username": "Emi2015",
            'password1': user2.password,
            'password2': user2.password,
        }
        self.client.force_login(user2)
        response = self.client.get(url, update_user)
        self.assertRedirects(response, reverse("users_list"))
        self.assertEqual(user2.username, "author")

    def test_user_delete(self):
        # Удаляем пользователя и проверяем количество оставшихся пользователей
        self.assertEqual(Users.objects.count(), 5)
        user5 = Users.objects.get(pk=5)
        self.client.force_login(user5)
        url = reverse("user_delete", args=[user5.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 4)

    def test_delete_user_without_permission(self):
        # Проверяем, что пользователь не может удалить другого пользователя без разрешения
        self.assertEqual(Users.objects.count(), 5)
        user4 = Users.objects.get(pk=5)
        user2 = Users.objects.get(pk=2)
        self.client.force_login(user2)
        url = reverse("user_delete", args=[user4.pk])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(Users.objects.count(), 5)
