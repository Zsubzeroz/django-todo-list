from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('toggle/<int:tarefa_id>/', views.toggle_status, name='toggle_status'),

    path('tags/', views.list_tags, name='list_tags'),
    path('tags/add/', views.add_tag, name='add_tag'),
    path('tags/update/<int:tag_id>/', views.update_tag, name='update_tag'),
    path('tags/delete/<int:tag_id>/', views.delete_tag, name='delete_tag'),

    path('add/', views.add_task, name='add_task'),
]