from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Notification(models.Model):
    """
    Модель уведомления
    user - пользователь, которому приходит уведомление
    sender - отправить уведомления
    type - тип уведомления
    message - текст сообщения
    is_read - прочитано ли уведомление, булево поле
    created_at - дата и время создания уведомления
    """

    class NotificationTypes(models.TextChoices):
        FRIEND_REQUEST = "friend_request", "Friend Request"
        SITE_MESSAGE = "site_message", "Site Message"

    user = models.ForeignKey(to=get_user_model(), related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(to=get_user_model(), related_name='related_notifications', null=True, blank=True,
                               on_delete=models.CASCADE)
    type = models.CharField(choices=NotificationTypes.choices, max_length=50)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.type} - {self.message}"
