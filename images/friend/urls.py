from . import views
from django.urls import path

app_name = 'friend'

urlpatterns = [
    # Отправить заявку в друзья
    path('send_friend_request/<int:receiver_id>', views.send_friend_request, name='send_friend_request'),
    # Отменить заявку в друзья
    path('cancel_friend_request/<int:receiver_id>', views.cancel_friend_request, name='cancel_friend_request'),
    # Принять заявку в друзья
    path('accept_friend_request/<int:sender_id>', views.accept_friend_request, name='accept_friend_request'),
    # Отменить заявку в друзья
    path('reject_friend_request/<int:sender_id>', views.reject_friend_request, name='reject_friend_request'),
]
