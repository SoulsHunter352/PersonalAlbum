from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from .models import Notification


# Create your views here.

class ShowNotifications(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notifications.html'
    context_object_name = 'notifications'
    extra_context = {'title': 'Уведомления'}
    allow_empty = True

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False).select_related('sender')
