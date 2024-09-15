from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='home'),  # Домашняя страница
    path("login/", views.login, name='login'),
    path("create_album/", views.create_album, name='create_album'),  # Создать альбом
    path("create_image/", views.AddImage.as_view(), name='create_image'),  # Создать изображение.
    # Добавить картинку в альбом
    path("<int:album_id>/create_image/", views.AddImageToAlbum.as_view(), name='add_image_to_album'),
    path("show_image/<int:image_id>/", views.ShowImage.as_view(), name='show_image'),  # Посмотреть картинку
    path("delete/<int:album_id>/<int:image_id>/", views.DeleteImage.as_view(), name='delete_image'),  # Удалить картинку
    path("edit/<int:image_id>/", views.EditImage.as_view(), name='update_image'),  # Изменить картинку
    path('albums/', views.ShowAlbums.as_view(), name='albums'),  # Посмотреть альбомы
    path('<int:album_id>/', views.ShowAlbumImages.as_view(), name='album_images'),  # Посмотреть картинки альбома
    path('edit/album/<int:album_id>/', views.UpdateAlbum.as_view(), name='edit'),  # Изменить альбом
    path('delete/album/<int:album_id>/', views.DeleteAlbum.as_view(), name='delete_album'),  # Удалить альбом
    path('change_visibility/<int:album_id>/', views.change_album_visibility,
         name='change_album_visibility'),  # Изменить видимость альбома
    path('change_image_visibility/<int:image_id>/', views.change_image_visibility,
         name='change_image_visibility')  # Изменить видимость картинки
]
