from django.contrib import admin
from .models import Parser
from .tasks import print_actor

@admin.action(description="Run selected parsers")
def run(modeladmin, request, queryset):
    for parser in queryset.all():
        print_actor.send(parser.name)

class ParserAdmin(admin.ModelAdmin):
    actions = [run]

admin.site.register(Parser, ParserAdmin)