from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.


class Albums(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название альбома', unique=True)  # Название альбома
    photo = models.ImageField(upload_to='photos/album_photos/', verbose_name='Обложка альбома',
                              blank=True, null=True, default=None)  # Обложка альбома
    author = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT, default=None, null=True,
                               related_name='albums')
    public = models.BooleanField(verbose_name='Публичный альбом', default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('album_images', kwargs={"album_id": self.id})


class Images(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название картинки')  # Название картинки
    photo = models.ImageField(upload_to='photos/images/', verbose_name='Изображение')  # Изображение
    content = models.TextField(max_length=250, blank=True, verbose_name='Подпись к картинке')  # Подпись к картинке
    album = models.ManyToManyField(to='Albums', related_name='images',
                                   verbose_name='Альбомы')  # Альбомы, в которые входит изображение
    author = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT, default=None, null=True,
                               related_name='images')
    public = models.BooleanField(verbose_name='Публичная картинка', default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_image', kwargs={'image_id': self.id})
