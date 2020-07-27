from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('edit<int:pk><str:mode><int:submit>', views.edit, name='edit'),
    path('allbook', views.allbook, name='allbook'),
    path('return_book', views.return_book, name='return_book'),
    path('register', views.register, name="register"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('manage', views.manage, name='manage'),
    path('admin_page', views.admin_page, name='admin_page')
]