from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView, ListView, CreateView, DetailView

from .forms import CreateAlbumForm, AddImageForm, EditImageForm, AddImageToAlbumForm
from .models import Albums, Images

import uuid

# Create your views here.


def add_suffix(image_name):
    ext = ''
    if '.' in image_name:
        ext = image_name[image_name.rindex('.'):]
        image_name = image_name[:image_name.rindex('.')]
    suffix = uuid.uuid4()
    return f"{image_name}_{suffix}{ext}"


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'main_pages/index.html', context={'title': 'Персональный альбом', })


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'main_pages/login.html', context={'title': 'Авторизация', })


@login_required
def create_album(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            new_album = form.save()
            # new_album.slug = 'album' + str(uuid.uuid4())
            new_album.author = request.user
            new_album.save()
            return redirect('albums')
    else:
        form = CreateAlbumForm()
    return render(request, 'main_pages/create_album.html', context={'title': 'Создать альбом',  'form': form})


class UpdateAlbum(LoginRequiredMixin, UpdateView):
    """
    Класс представления для обновления альбома
    """
    model = Albums
    # fields = ['name', 'photo', 'public']
    form_class = CreateAlbumForm
    template_name = 'main_pages/create_album.html'
    extra_context = {'title': 'Изменить альбом'}
    success_url = reverse_lazy('albums')
    pk_url_kwarg = 'album_id'

    def form_valid(self, form):
        if 'photo' in form.changed_data:
            self.get_object().photo.delete()
            album = form.save(commit=False)
            album.photo.name = add_suffix(album.photo.name)
        return super().form_valid(form)


class DeleteAlbum(LoginRequiredMixin, DeleteView):
    """
    Класс представления для удаления альбома
    """
    success_url = reverse_lazy('albums')
    model = Albums

    def get_object(self, queryset=None):
        return get_object_or_404(Albums, id=self.kwargs['album_id'], author=self.request.user)


@login_required
def change_album_visibility(request: HttpRequest, album_id):
    """
    Изменение параметра видимости альбома
    :param request:
    :param album_id:
    :return:
    """
    if request.method == 'POST':
        album = get_object_or_404(Albums, pk=album_id)
        album.public = not album.public
        album.save()
        return JsonResponse({'new_visibility': album.public})


@login_required
def change_image_visibility(request: HttpRequest, image_id):
    """
    Изменение параметра видимости картинки
    :param request:
    :param image_id:
    :return:
    """
    if request.method == 'POST':
        image = get_object_or_404(Images, pk=image_id, author=request.user)
        image.public = not image.public
        image.save()
        return JsonResponse({'new_visibility': image.public})


@login_required
def add_image(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()
            # new_image.slug = uuid.uuid4()
            new_image.save()
    else:
        form = AddImageForm()
    return render(request, 'main_pages/new_image.html', context={'title': 'Добавить изображение',  'form': form})


class AddImage(CreateView):
    template_name = 'main_pages/new_image.html'
    form_class = AddImageForm
    extra_context = {'title': 'Добавить картинку'}

    def form_valid(self, form):
        new_image = form.save(commit=False)
        # new_image.slug = uuid.uuid4()
        new_image.author = self.request.user
        return super().form_valid(form)


class ShowAlbums(LoginRequiredMixin, ListView):
    """
    Класс представления списка альбомов пользователя
    """
    template_name = 'main_pages/albums.html'
    extra_context = {'title': 'Ваши альбомы'}
    context_object_name = 'albums'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'u' in self.request.GET:  # Если смотрим чужие альбомы
            context['title'] = f"Альбомы пользователя {self.request.GET.get('u')}"
            context['is_self'] = self.request.user.username == self.request.GET.get('u')
            context['username'] = self.request.GET.get('u')
        else:  # Если смотрим свои альбомы
            context['is_self'] = True
        return context

    def get_queryset(self):
        user = self.request.user
        if 'u' in self.request.GET:  # Если есть параметр имя пользователя
            if user.username != self.request.GET.get('u'):   # Если смотрим чужие альбомы
                # Получаем пользователя
                user = get_object_or_404(get_user_model(), username=self.request.GET.get('u'))
                albums = user.albums.filter(public=True)  # Получаем публичные альбомы
                if albums.count() == 0:  # Если нет публичных альбомов, то кидаем ошибку
                    raise Http404()
                return albums  # Если все хорошо, то идем дальше
        return user.albums.all()  # Если смотрим свои альбомы, то просто возвращаем альбомы

    def get(self, request, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            pass
        else:
            return super().get(request, *args, **kwargs)


class ShowAlbumImages(LoginRequiredMixin, ListView):
    """
    Класс представления изображений альбома
    Для просмотра чужих изображений используется параметр строки запроса u, который
    обозначает имя пользователя
    """
    template_name = 'main_pages/images.html'
    context_object_name = 'images'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # album = get_object_or_404(Albums, slug=self.kwargs['album_slug'], author=self.request.user)
        album = get_object_or_404(Albums, id=self.kwargs['album_id'])
        if 'u' in self.request.GET:
            # Если альбом непубличный и не принадлежит пользователю
            if not album.public and self.request.user.username != self.request.GET.get('u'):
                raise Http404()
            context['is_self'] = self.request.user.username == self.request.GET.get('u')
            context['username'] = self.request.GET.get('u')
        elif album.author != self.request.user:  # Если нет параметра u и мы смотрим чужой альбом
            raise Http404()  # Генерируем ошибку
        else:
            context['is_self'] = True
        context['title'] = album.name
        context['album_slug'] = album.id
        return context

    def get_queryset(self):
        if 'u' in self.request.GET:  # Если есть параметр имени пользователя
            if self.request.user.username != self.request.GET.get('u'):  # Если смотрим чужую картинку
                # Получаем только публичные
                return Images.objects.filter(album__id=self.kwargs['album_id'], public=True)
        # Если смотрим свои изображения, то получаем все изображения
        return Images.objects.filter(album__id=self.kwargs['album_id'], author=self.request.user)


class AddImageToAlbum(LoginRequiredMixin, CreateView):
    """
    Класс представления для создания картинки внутри альбома
    """
    form_class = AddImageToAlbumForm
    template_name = 'main_pages/new_image.html'
    extra_context = {'title': 'Добавить картинку'}

    def form_valid(self, form):
        new_image = form.save(commit=False)
        # new_image.slug = uuid.uuid4()  # Генерируем слаг для картинки
        new_image.author = self.request.user  # Устанавливаем автора
        new_image.save()
        form.save_m2m()
        new_image.album.add(self.album.id)  # Добавляем m2m связь к альбому
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(Albums, id=kwargs['album_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class ShowImage(LoginRequiredMixin, DetailView):
    """
    Класс представления просмотра картинки из альбома
    """
    context_object_name = 'image'
    template_name = 'main_pages/image.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['image'].title
        album = get_object_or_404(Albums, images=context['image'].id)
        context['album_id'] = album.id
        if 'u' in self.request.GET and album.public:  # Если есть параметр и альбом публичный
            context['is_self'] = self.request.user.username == self.request.GET.get('u')
        elif context['image'].author != self.request.user:  # Если не автор этой картинки пытается посмотреть
            raise Http404()  # Выбрасываем ошибку
        else:
            context['is_self'] = True
        return context

    def get_object(self, queryset=None):
        """
        Получаем изображение если оно существует
        :param queryset:
        :return:
        """
        if 'u' in self.request.GET:  # Если смотрим чужую картинку
            image = get_object_or_404(Images, id=self.kwargs['image_id'], public=True)
        else:
            image = get_object_or_404(Images, id=self.kwargs['image_id'])
        return image


class DeleteImage(LoginRequiredMixin, DeleteView):
    """
    Класс представления для удаления картинки
    """
    model = Images

    def get_object(self, queryset=None):
        """
        Получаем изображение, которое хотят удалить и проверяем, что его создал текущий пользователь
        :param queryset:
        :return:
        """
        image = get_object_or_404(Images, id=self.kwargs['image_id'], author=self.request.user)
        return image

    def form_valid(self, form):
        """
        Переопределяем success_url в зависимости от альбома к которому принадлежит картинка
        :param form:
        :return:
        """
        self.success_url = reverse_lazy('album_images', kwargs={'album_id': self.kwargs['album_id']})
        self.object.photo.delete()
        self.object.delete()
        # print(self.object.photo.url)
        return HttpResponseRedirect(self.success_url)


class EditImage(UpdateView):
    template_name = 'main_pages/new_image.html'
    form_class = AddImageToAlbumForm
    extra_context = {'title': 'Изменить картинку'}

    def form_valid(self, form):
        """
        В случае загрузки новой картинки удаляем старую и вызываем родительский метод
        :param form:
        :return:
        """
        if 'photo' in form.changed_data:
            self.get_object().photo.delete()  # Удаляем старое фото
            image = form.save(commit=False)
            image.photo.name = add_suffix(image.photo.name)  # Добавляем суффикс к имени картинки
        return super().form_valid(form)

    def get_object(self, queryset=None):
        image = get_object_or_404(Images, id=self.kwargs['image_id'], author=self.request.user)
        return image
