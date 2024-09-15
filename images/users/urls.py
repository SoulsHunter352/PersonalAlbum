from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registrate/', views.RegistrateUserView.as_view(), name='registrate'),
    path('password_change/', views.UserChangePassword.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('search_users/', views.UsersSearch.as_view(), name='search_users'),
    path('update_profile', views.UserUpdateProfile.as_view(), name='update_profile'),
    path('<slug:username>/', views.ShowUserProfile.as_view(), name='profile'),
]
