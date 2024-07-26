# from django.test import TestCase, Client
# from task_manager.labels.models import Label
# from task_manager.users.models import Users
# from django.urls import reverse
#
#
# class LabelsTest(TestCase):
#
#     fixtures = ["labels.json", "users.json"]
#
#     def setUp(self):
#         self.client = Client()
#         self.label = Label.objects.create(name='Huk')
#         self.user = Users.objects.get(pk="5")
#         self.client.force_login(self.user)
#
#     def test_label_exist(self):
#         self.assertEqual(Label.objects.count(), 3)
#
#     def test_label_create(self):
#         new_label = {
#             'name': 'Hak',
#         }
#         response = self.client.post(reverse('label_create'), data=new_label)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Label.objects.count(), 4)
#
#     def test_read(self):
#         response = self.client.get(reverse('labels'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.label.name)
#
#     def test_label_update(self):
#         update_label = {"name": "Huuuuuk"}
#         label1 = Label.objects.get(pk="2")
#         url = reverse("label_update", args=[label1.pk])
#         response = self.client.post(url, update_label)
#         self.assertEqual(response.status_code, 302)
#         label1.refresh_from_db()
#         self.assertEqual(label1.name, update_label["name"])
#
#     def test_label_delete(self):
#         label2 = Label.objects.get(pk="2")
#         url = reverse("label_delete", args=[label2.pk])
#         response = self.client.post(url)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Label.objects.count(), 2)
