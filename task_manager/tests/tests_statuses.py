from django.test import TestCase, Client
from task_manager.statuses.models import Status
from task_manager.users.models import Users
from django.urls import reverse


class StatusesTest(TestCase):

    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.user = Users.objects.get(pk=5)
        self.client.force_login(self.user)
        print(f"Initial status count: {Status.objects.count()}")
        print("Statuses in the database:")
        for status in Status.objects.all():
            print(f"Status {status.pk}: {status.name}")

    def test_statuses_exist(self):
        count = Status.objects.count()
        print(f"Number of statuses: {count}")
        self.assertEqual(count, 2)

    def test_status_create(self):
        new_status = {'name': 'Spring'}
        response = self.client.post(reverse('status_create'), data=new_status)
        print(f"Create status response: {response.status_code}")
        print(f"Statuses after creation: {Status.objects.count()}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 3)

    def test_status_read(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anna_Smir')
        self.assertContains(response, 'Masha_Iv')

    def test_status_update(self):
        update_status = {"name": "Summer"}
        status1 = Status.objects.get(pk=1)
        url = reverse("status_update", args=[status1.pk])
        response = self.client.post(url, update_status)
        print(f"Update status response: {response.status_code}")
        status1.refresh_from_db()
        self.assertEqual(status1.name, update_status["name"])

    def test_status_delete(self):
        status2 = Status.objects.get(pk=2)
        url = reverse("status_delete", args=[status2.pk])
        response = self.client.post(url)
        print(f"Delete status response: {response.status_code}")
        print(f"Statuses after deletion: {Status.objects.count()}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 1)
