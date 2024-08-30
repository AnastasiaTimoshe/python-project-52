from django.test import TestCase, Client
from task_manager.tasks.models import Task
from task_manager.users.models import Users
from task_manager.statuses.models import Status
from django.urls import reverse


class TasksTest(TestCase):

    fixtures = ["users.json", "statuses.json"]

    def setUp(self):
        self.client = Client()

        self.user = Users.objects.get(pk=5)
        self.client.force_login(self.user)

        self.status = Status.objects.get(pk=2)

        self.task = Task.objects.create(
            name="Task 7",
            description="Description of Task 7",
            status=self.status,
            executor=self.user
        )
        self.task_to_delete = Task.objects.create(
            name="Task to delete",
            description="Description of Task to delete",
            status=self.status,
            executor=self.user
        )

    def test_tasks_exist(self):
        self.assertEqual(Task.objects.count(), 2)

    def test_task_create(self):
        user1 = Users.objects.get(pk=2)
        status1 = Status.objects.get(pk=2)
        new_task = {
            "name": "To write test",
            "description": "please, write tests",
            "status": status1.pk,
            "executor": user1.pk,
            "label": "",
        }
        url = reverse("task_create")
        response = self.client.post(url, new_task)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 3)

    def test_task_read(self):
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_update(self):
        user1 = Users.objects.get(pk=2)
        status1 = Status.objects.get(pk=2)
        update_task = {
            "name": "To write test",
            "description": "it's necessarily",
            "status": status1.pk,
            "executor": user1.pk,
            "label": "",
        }
        url = reverse("task_update", args=[self.task.pk])
        response = self.client.post(url, update_task)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.description, update_task["description"])

    def test_task_delete(self):
        url = reverse("task_delete", args=[self.task_to_delete.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
