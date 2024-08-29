from django.test import TestCase
from django.core.management import call_command
from task_manager.labels.models import Label
from django.urls import reverse
from task_manager.users.models import Users


class LabelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'labels.json', 'users.json')
        print("Фикстуры загружены")

    def setUp(self):
        initial_count = Label.objects.count()
        print(f"Начальное количество меток: {initial_count}")

        # Авторизуем пользователя для выполнения удаления
        self.user = Users.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        super().setUp()

    def test_label_exist(self):
        expected_count = 3
        actual_count = Label.objects.count()
        self.assertEqual(actual_count, expected_count, f"Expected {expected_count} labels, found {actual_count}")

    def test_label_create(self):
        new_label = {'name': 'New Label'}
        response = self.client.post(reverse('label_create'), data=new_label)
        self.assertEqual(response.status_code, 302, "Create label did not redirect as expected")
        self.assertEqual(Label.objects.count(), 4, "Label count did not increase after creation")

    def test_label_delete(self):
        # Создать метку, которую затем удалим
        label_to_delete = Label.objects.create(name="To be deleted")

        # Убедитесь, что метка создана
        self.assertEqual(Label.objects.count(), 4, "Label count did not increase after creating new label")

        # Выполнить удаление метки
        response = self.client.post(reverse('label_delete', args=[label_to_delete.pk]))

        # Убедитесь, что удаление метки прошло успешно и произошёл редирект
        self.assertEqual(response.status_code, 302, "Delete did not redirect as expected")

        # Проверяем, что количество меток уменьшилось на 1
        self.assertEqual(Label.objects.count(), 3, "Label count did not decrease after deletion")
