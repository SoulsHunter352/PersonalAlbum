from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import LoginForm, RegisterUserForm, UserChangePasswordForm, UserUpdateForm
from django.shortcuts import get_object_or_404

from .utils import AnonymousRequiredMixin
from friend.models import FriendsList, FriendRequest

import enum


class FriendRequestStatus(enum.Enum):
    YOU_SENT_TO_THEM = -1
    NO_REQUEST_SENT = 0
    THEM_SENT_YOU = 1

# Create your views here.


class LoginUserView(AnonymousRequiredMixin, LoginView):
    """
    Класс представления для авторизации пользователя
    """
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegistrateUserView(AnonymousRequiredMixin, CreateView):
    """
    Класс представления для регистрации пользователя
    """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    model = get_user_model()
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('albums')

    def form_valid(self, form):
        user = form.save()
        FriendsList.objects.create(user=user)  # Создаем список друзей для данного пользователя
        return super().form_valid(form)


class ShowUserProfile(DetailView):
    """
    Класс представления для отображения профиля пользователя
    """
    template_name = 'users/account.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['profile'].username
        # Свой профиль смотрим или чужой
        context['is_self'] = True if self.request.user == context['profile'] else False
        context['cnt_albums'] = context['profile'].albums.count() if self.request.user == context['profile'] \
            else context['profile'].albums.filter(public=True).count()  # Количество альбомов
        if FriendsList.objects.filter(user=context['profile']).exists():  # Проверяем есть ли список друзей
            context['cnt_friends'] = context['profile'].friends.count()  # Получаем количество друзей
        else:
            FriendsList.objects.create(user=context['profile'])  # Создаем список друзей если его нет
            context['cnt_friends'] = 0  # Записываем количество друзей
        if not context['is_self'] and self.request.user.is_authenticated:
            context['is_auth'] = True
            if FriendsList.objects.get(user=self.request.user).friends.filter(pk=context['profile'].id):
                context['is_friend'] = True  # Если друзья, то отмечаем это
            else:
                context['is_friend'] = False  # Если не друзья
                # Если мы отправили запрос в друзья
                if FriendRequest.objects.filter(sender=self.request.user, receiver=context['profile']).exists():
                    context['request_status'] = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # Если нам отправили запрос в друзья
                elif FriendRequest.objects.filter(sender=context['profile'], receiver=self.request.user).exists():
                    context['request_status'] = FriendRequestStatus.THEM_SENT_YOU.value
        else:
            context['is_auth'] = False
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(get_user_model(), username=self.kwargs['username'])


class UserChangePassword(LoginRequiredMixin, PasswordChangeView):
    """
    Класс представления для изменения пароля
    """
    template_name = 'users/password_change.html'
    extra_context = {'title': 'Изменить пароль'}
    form_class = UserChangePasswordForm
    success_url = reverse_lazy('users:password_change_done')


class UsersSearch(ListView):
    """
    Класс представления результатов поиска пользователей
    """
    model = get_user_model()
    context_object_name = 'profiles'  # переменная для найденных профилей
    template_name = 'users/search_profiles.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Результаты поиска по запросу {self.request.GET.get('q')}"
        return context

    def get_queryset(self):
        return get_user_model().objects.filter(username__icontains=self.request.GET.get('q'))


class UserUpdateProfile(LoginRequiredMixin, UpdateView):
    """
    Класс представления для обновления данных пользователя
    """
    form_class = UserUpdateForm
    model = get_user_model()
    template_name = 'users/update_account.html'

    def form_valid(self, form):
        self.success_url = reverse_lazy('users:profile', kwargs={'username': self.request.user.username})
        if 'photo' in form.changed_data:
            if self.get_object().photo:
                self.get_object().photo.delete()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user
