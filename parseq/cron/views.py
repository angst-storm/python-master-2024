from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    """Представление, которое перенаправляет
    любой запрос на страницу администратора Django"""
    return redirect(reverse("admin:index"))
