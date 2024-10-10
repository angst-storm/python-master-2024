from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test"

    def handle(self, *args, **options):
        print("APScheduler runned")