from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AnonymousRequiredMixin(AccessMixin):
    """
    Миксин для страниц, которые доступны только пользователям,
    не вошедшим в профиль.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('albums'))
        return super().dispatch(request, *args, **kwargs)