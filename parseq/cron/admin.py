from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_dramatiq.admin import TaskAdmin
from django_dramatiq.models import Task
from dramatiq import Message

from .models import Parser
from .tasks import send_run_actor

TIME_TEMPLATE = "%d %b %Y %H:%M:%S"


def get_args(task):
    """Возвращает массив аргументов запуска актора Task."""
    return Message.decode(bytes(task.message_data)).args


@admin.action(description="Run selected parsers")
def run(modeladmin, request, queryset):
    """Admin Action, cтавит в очередь Dramatiq все выделенные парсеры."""
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
    list_display = ("_run_id", "status", "_created", "_updated", "_parser_id")

    def _run_id(self, instance):
        return get_args(instance)[0]

    def _parser_id(self, instance):
        """Возвращает ссылку на запущенный парсер."""
        parser_id = get_args(instance)[1]
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:cron_parser_change", args=(parser_id,)),
            parser_id,
        )

    def _created(self, instance):
        return instance.created_at.strftime(TIME_TEMPLATE)

    def _updated(self, instance):
        return instance.updated_at.strftime(TIME_TEMPLATE)


admin.site.unregister(Task)
admin.site.register(Task, NewTaskAdmin)
admin.site.register(Parser, ParserAdmin)
