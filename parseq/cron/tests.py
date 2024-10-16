from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse
from django_dramatiq.models import Task
from dramatiq import Message

from .models import Parser


class CronTestCase(TestCase):
    def setUp(self):
        self.username = "admin"
        self.password = "admin"
        self.user = User.objects.create_superuser(
            self.username, "admin@example.com", self.password
        )
        f = open("../parsers/httpcat.py")
        path = default_storage.save("test/httpcat.py", File(f))
        self.parser = Parser.objects.create(
            name="httpcat",
            description="Download random image with HTTP Cat.",
            script=path,
        )

    def test_parser_manual_run(self):
        data = {"action": "run", "_selected_action": self.parser.id}
        change_url = reverse("admin:cron_parser_changelist")
        self.client.login(username=self.username, password=self.password)
        self.client.post(change_url, data)
        self.client.logout()
        tasks = Task.tasks.all()
        self.assertTrue(len(tasks) > 0)
        task_message = Message.decode(bytes(tasks.first().message_data))
        self.assertEqual(task_message.args[1], self.parser.id)
