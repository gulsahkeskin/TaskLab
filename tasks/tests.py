from django.contrib.auth.models import User

from django.test import TestCase

from tasks.models import Task


class UrlResponse(TestCase):

    def test_home_url_response_ok(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_login_url_response_ok(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url_response_ok(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)


class TaskTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username="gulsah", password="123")
        Task.objects.create(user_id=1, title="title", memo="some text", progress=True)

    # def setUp(self):
    #     self.user = User.objects.create_user(username='testuser', password='12345')
    #     Task.objects.create(title="title", memo="some text", progress=True, user=request.)

    def test_task_is_created_successfully(self):
        task = Task.objects.create(title="some title", memo="explanations", progress=True)
        self.assertEqual(task.title, "some title")
        self.assertEqual(task.user_id, 123)
        self.assertEqual(task.memo, "explanations")
        self.assertEqual(task.progress, True)
