from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.homepage_view, name='homepage'),
    path('add/', views.add_todo, name='add_todo'),
    path('todos/<int:pk>/edit/', views.edit_todo, name='edit_todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),
    path('taskboard/', views.taskboard_view, name='taskboard'),
    path('update-status/', views.update_status_view, name='update_status'),
]
