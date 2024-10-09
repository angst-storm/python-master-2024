from django.contrib import admin
from .models import Parser
from .tasks import run_actor

@admin.action(description="Run selected parsers")
def run(modeladmin, request, queryset):
    for parser in queryset.all():
        run_actor.send(parser.name, parser.script.path)

class ParserAdmin(admin.ModelAdmin):
    actions = [run]

admin.site.register(Parser, ParserAdmin)