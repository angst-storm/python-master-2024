from django.contrib import admin
from .models import Parser
from .tasks import send_run_actor
from django_dramatiq.models import Task
from django_dramatiq.admin import TaskAdmin
from dramatiq import Message
from django.urls import reverse
from django.utils.html import format_html

@admin.action(description="Run selected parsers")
def run(modeladmin, request, queryset):
    for parser in queryset.all():
        send_run_actor(parser.id, parser.name, parser.script.path)

class ParserAdmin(admin.ModelAdmin):
    list_display = ('name', 'script', 'scheduled', 'repeat_after')
    list_display_links = ('name',)
    actions = [run]

class NewTaskAdmin(TaskAdmin):
    list_display = ('run_id', 'status', "created_at", "updated_at", 'parser')
    
    def run_id(self, instance):
        return Message.decode(bytes(instance.message_data)).args[0]
    
    def parser(self, instance):
        args = Message.decode(bytes(instance.message_data)).args
        return format_html('<a href="{}">{}</a>', reverse("admin:cron_parser_change", args=(args[1],)), args[2])

admin.site.unregister(Task)
admin.site.register(Task, NewTaskAdmin)
admin.site.register(Parser, ParserAdmin)