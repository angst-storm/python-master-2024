from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    """Перенаправляет любой запрос на страницу администратора Django."""
    return redirect(reverse("admin:index"))
