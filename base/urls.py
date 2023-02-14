from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name= 'login'),
    path('register/', views.registerPage, name= 'register'),
    path('logout/', views.logoutPage, name= 'logout'),
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('profile/<str:pk>', views.user_profile, name='user_profile'),
    path('create_room/', views.create_room, name='create_room'),
    path('update_room/<str:pk>/', views.update_room, name='update_room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete_room'),
    path('delete_message/<str:pk>/', views.delete_message, name='delete_message'),
    path('update_user/', views.update_user, name='update_user'),
    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
]

