from django.contrib import admin
from .models import Parser
from .tasks import send_run_actor
import uuid

@admin.action(description="Run selected parsers")
def run(modeladmin, request, queryset):
    for parser in queryset.all():
        send_run_actor(parser.name, parser.script.path)

class ParserAdmin(admin.ModelAdmin):
    list_display = ('name', 'script', 'scheduled', 'repeat_after')
    list_display_links = ('name',)
    actions = [run]

admin.site.register(Parser, ParserAdmin)