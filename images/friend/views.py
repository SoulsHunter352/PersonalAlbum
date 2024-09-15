from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404

from friend.models import FriendRequest


# Create your views here.

@login_required
def friend_request_message(request: HttpRequest, receiver_id: int):
    """
    Метод представления для отправления заявки.
    Используется метод POST, в котором обязательным параметром является action.
    action принимает два значения: send - отправить заявку, cancel - отменить заявку
    :param request:
    :param receiver_id:
    :return:
    """
    if request.method == 'POST':
        sender = request.user
        receiver = get_object_or_404(get_user_model(), pk=receiver_id)
        if request.POST.get('action') == 'send':  # Если действие отправить заявку в друзья
            if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():  # Проверяем на уже отправленные
                return JsonResponse({'is_success': False, 'message': 'Friend request already exists'})
            FriendRequest.objects.create(sender=sender, receiver=receiver)  # Если нет создаем новую заявку
            return JsonResponse({'is_success': True, 'status': 'send'})
        elif request.POST.get('action') == 'cancel':  # Если действие удалить заявку в друзья
            if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():  # Проверяем существование заявки
                FriendRequest.objects.get(sender=sender, receiver=receiver).cancel()  # Удаляем заявку
                return JsonResponse({'is_success': True, 'status': 'delete'})
            return JsonResponse({'is_success': False, 'message': 'No exists friend request'})


@login_required
def send_friend_request(request: HttpRequest, receiver_id: int):
    """
    Отправка заявки в друзья
    :param request:
    :param receiver_id:
    :return:
    """
    if request.method == 'POST':
        sender = request.user
        receiver = get_object_or_404(get_user_model(), pk=receiver_id)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():  # Проверяем на уже отправленные
            return JsonResponse({'is_success': False, 'message': 'Friend request already send'})
        FriendRequest.objects.create(sender=sender, receiver=receiver)  # Если нет создаем новую заявку
        return JsonResponse({'is_success': True, 'status': 'delete'})


@login_required
def cancel_friend_request(request: HttpRequest, receiver_id: int):
    """
    Удаление заявки в друзья
    :param request:
    :param receiver_id:
    :return:
    """
    if request.method == 'POST':
        sender = request.user
        receiver = get_object_or_404(get_user_model(), pk=receiver_id)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():  # Проверяем на существование заявки
            FriendRequest.objects.get(sender=sender, receiver=receiver).cancel()
            return JsonResponse({'is_success': True, 'status': 'send'})
        return JsonResponse({'is_success': False, 'message': 'No such friend request'})


@login_required
def accept_friend_request(request: HttpRequest, sender_id: int):
    """
    Принять заявку в друзья
    :param request:
    :param sender_id:
    :return:
    """
    if request.method == 'POST':
        receiver = request.user
        sender = get_object_or_404(get_user_model(), pk=sender_id)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            FriendRequest.objects.get(sender=sender, receiver=receiver).accept()
            return JsonResponse({'is_success': True, 'status': 'friends'})
        return JsonResponse({'is_success': False, 'message': 'No such friend request'})


@login_required
def reject_friend_request(request: HttpRequest, sender_id: int):
    """
    Отклонить заявку в друзья
    :param request:
    :param sender_id:
    :return:
    """
    if request.method == 'POST':
        receiver = request.user
        sender = get_object_or_404(get_user_model(), pk=sender_id)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            FriendRequest.objects.get(sender=sender, receiver=receiver).reject()
            return JsonResponse({'is_success': True, 'status': 'not friends'})
        return JsonResponse({'is_success': False, 'message': 'No such friend request'})
