from django.test import TestCase
from .models import Parser
from django_dramatiq.models import Task
from django.contrib.auth.models import User
from django.urls import reverse


class CronTestCase(TestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_superuser(self.username, 'admin@example.com', self.password)
        self.parser = Parser.objects.create(
            name="httpcat", 
            description="Download random image with HTTP Cat.", 
            script='../../parsers/httpcat.py'
        )

    def test_parser_manual_run(self):
        data = {'action': 'run', '_selected_action': self.parser.id}
        change_url = reverse('admin:cron_parser_changelist')
        self.client.login(username=self.username, password=self.password)        
        response = self.client.post(change_url, data)
        self.client.logout()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Task.objects.all()), 1)