from django.test import TestCase
from django.core.management import call_command
from task_manager.labels.models import Label
from django.urls import reverse
from task_manager.users.models import Users


class LabelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'labels.json', 'users.json')

    def setUp(self):
        self.user = Users.objects.create_user(username='tester', password='password')
        self.client.login(username='tester', password='password')

    def test_label_exist(self):
        expected_count = 3
        actual_count = Label.objects.count()
        self.assertEqual(actual_count, expected_count,
                         f"Expected {expected_count} labels, found {actual_count}")

    def test_label_create(self):
        new_label = {'name': 'New Label'}
        response = self.client.post(reverse('label_create'), data=new_label)
        self.assertEqual(response.status_code, 302, "Create label did not redirect as expected")
        self.assertEqual(Label.objects.count(), 4, "Label count did not increase after creation")
        self.assertTrue(Label.objects.filter(name='New Label').exists(),
                        "New label was not created")

    def test_label_delete(self):
        label_to_delete = Label.objects.create(name="To be deleted")

        self.assertEqual(Label.objects.count(), 4,
                         "Label count did not increase after creating new label")

        response = self.client.post(reverse('label_delete', args=[label_to_delete.pk]))

        self.assertEqual(response.status_code, 302, "Delete did not redirect as expected")

        self.assertEqual(Label.objects.count(), 3, "Label count did not decrease after deletion")
