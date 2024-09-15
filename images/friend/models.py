from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class FriendsList(models.Model):
    """
    Модель списка друзей пользователя

    user - пользователь
    friends - список друзей
    """
    user = models.OneToOneField(to=get_user_model(), related_name='user', on_delete=models.CASCADE)
    friends = models.ManyToManyField(to=get_user_model(), related_name='friends', blank=True)

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Добавление в друзья
        :param account:
        :return:
        """
        self.friends.add(account)
        self.save()

    def remove_friend(self, account):
        """
        Удаление из друзей
        :param account:
        :return:
        """
        if account in self.friends:
            self.friends.remove(account)
            self.save()

    def is_friend(self, account):
        """
        Проверка к принадлежности к друзьям
        :param account:
        :return:
        """
        return account in self.friends


class FriendRequest(models.Model):
    """
    Модель заявки в друзья

    sender - отправитель заявки в друзья
    recipient - пользователя, с которым хотят стать друзьями
    create - время создания
    is_active - принята ли заявка в друзья
    """
    sender = models.ForeignKey(to=get_user_model(), related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(to=get_user_model(), related_name='receiver', on_delete=models.CASCADE)
    create = models.DateField(auto_now_add=True)
    is_accepted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Принять заявку в друзья
        :return:
        """
        sender_friends_list = FriendsList.objects.get(user=self.sender)  # Список друзей отправителя
        receiver_friends_list = FriendsList.objects.get(user=self.receiver)  # Список друзей получателя
        sender_friends_list.add_friend(self.receiver)  # Добавляем в друзья получателя
        receiver_friends_list.add_friend(self.sender)  # Добавляем в друзья отправителя
        self.is_accepted = True
        self.delete()

    def reject(self):
        """
        Отклонить запрос
        :return:
        """
        self.delete()

    def cancel(self):
        """
        Отменить запрос
        :return:
        """
        self.delete()
