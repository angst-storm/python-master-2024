from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_dramatiq.admin import TaskAdmin
from django_dramatiq.models import Task
from dramatiq import Message

from .models import Parser
from .tasks import send_run_actor

TIME_TEMPLATE = "%d %b %Y %H:%M:%S"


@admin.action(description="Run selected parsers")
def run(modeladmin, request, queryset):
    """Django Admin Action, который cтавит в очередь Dramatiq все выделенные парсеры."""
    for parser in queryset.all():
        send_run_actor(parser.id)


class ParserAdmin(admin.ModelAdmin):
    list_display = ("name", "script", "_scheduled_at", "repeat_after")
    list_display_links = ("name",)
    actions = [run]

    def _scheduled_at(self, instance):
        scheduled = instance.scheduled
        return None if scheduled is None else scheduled.strftime(TIME_TEMPLATE)


class NewTaskAdmin(TaskAdmin):
    list_display = ("_run_id", "status", "_created", "_updated", "_parser")

    def _run_id(self, instance):
        return Message.decode(bytes(instance.message_data)).args[0]

    def _parser(self, instance):
        """Возвращает ссылку на запущенный парсер."""
        parser_id = Message.decode(bytes(instance.message_data)).args[1]
        parser = Parser.objects.get(id=parser_id)
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:cron_parser_change", args=(parser_id,)),
            parser.name,
        )

    def _created(self, instance):
        return instance.created_at.strftime(TIME_TEMPLATE)

    def _updated(self, instance):
        return instance.updated_at.strftime(TIME_TEMPLATE)


admin.site.unregister(Task)
admin.site.register(Task, NewTaskAdmin)
admin.site.register(Parser, ParserAdmin)
