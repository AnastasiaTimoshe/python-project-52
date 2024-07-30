from django.test import TestCase, Client
from task_manager.statuses.models import Status
from task_manager.users.models import Users
from django.urls import reverse


class StatusesTest(TestCase):

    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.status = Status.objects.create(name='Winter')
        self.user = Users.objects.get(pk="5")
        self.client.force_login(self.user)

    def test_statuses_exist(self):
        self.assertEqual(Status.objects.count(), 4)

    def test_status_create(self):
        new_status = {
            'name': 'Spring',
        }
        response = self.client.post(reverse('status_create'), data=new_status)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 5)

    def test_status_read(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

    def test_status_update(self):
        update_status = {"name": "Summer"}
        status1 = Status.objects.get(pk="2")
        url = reverse("status_update", args=[status1.pk])
        response = self.client.post(url, update_status)
        self.assertEqual(response.status_code, 302)
        status1.refresh_from_db()
        self.assertEqual(status1.name, update_status["name"])

    def test_status_delete(self):
        status2 = Status.objects.get(pk="3")
        url = reverse("status_delete", args=[status2.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 3)
