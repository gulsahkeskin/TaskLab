from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse

from tasks.forms import TaskForm
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


class TaskModelTest(TestCase):

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        # Create a task
        task = Task.objects.create(title='some title', memo='explanations', progress=True)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('current_tasks'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'tasks/current.html')

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Task.objects.create(title='docker', memo='compose')

    def test_task_created_successfully(self):
        print("task named successfully")
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        field_memo = task._meta.get_field('memo').verbose_name
        self.assertEqual(field_label, 'title')
        self.assertEqual(field_memo, 'memo')

    def test_create_new_task_form(self):
        form_data = {'title': 'test task title', 'memo': 'test details', }
        test_form = TaskForm(form_data)
        self.assertTrue(test_form.is_valid())
        test_form.save()
