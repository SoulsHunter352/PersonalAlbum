
menu = [
    {'title': 'Главная', 'url_name': 'home', 'for_guest': True},
    {'title': 'Главная', 'url_name': 'home', 'for_guest': False},
    {'title': 'Альбомы', 'url_name': 'albums', 'for_guest': False},
    {'title': 'Регистрация', 'url_name': 'users:registrate', 'for_guest': True},
    {'title': 'Войти', 'url_name': 'users:login', 'for_guest': True},
]


def get_base_menu(request):
    return {'menu': menu}
