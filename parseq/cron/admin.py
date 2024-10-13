from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_dramatiq.admin import TaskAdmin
from django_dramatiq.models import Task
from dramatiq import Message

from .models import Parser
from .tasks import send_run_actor

time_template = "%d %b %Y %H:%M:%S"


@admin.action(description="Run selected parsers")
def run(modeladmin, request, queryset):
    for parser in queryset.all():
        send_run_actor(parser.id, parser.name, parser.script.path)


class ParserAdmin(admin.ModelAdmin):
    list_display = ("name", "script", "_scheduled_at", "repeat_after")
    list_display_links = ("name",)
    actions = [run]

    def _scheduled_at(self, instance):
        scheduled = instance.scheduled
        return None if scheduled is None else scheduled.strftime("%d %b %Y %H:%M:%S")


class NewTaskAdmin(TaskAdmin):
    list_display = ("run_id", "status", "created", "updated", "parser")

    def run_id(self, instance):
        return Message.decode(bytes(instance.message_data)).args[0]

    def parser(self, instance):
        args = Message.decode(bytes(instance.message_data)).args
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:cron_parser_change", args=(args[1],)),
            args[2],
        )

    def created(self, instance):
        return instance.created_at.strftime("%d %b %Y %H:%M:%S")

    def updated(self, instance):
        return instance.updated_at.strftime("%d %b %Y %H:%M:%S")


admin.site.unregister(Task)
admin.site.register(Task, NewTaskAdmin)
admin.site.register(Parser, ParserAdmin)
