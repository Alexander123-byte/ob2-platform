from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)

app_name = 'content'

urlpatterns = [
    # Главная страница со списком постов
    path('', PostListView.as_view(), name='post_list'),

    # Просмотр отдельного поста
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Создание поста
    path('post/create/', PostCreateView.as_view(), name='post_create'),

    # Редактирование поста
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),

    # Удаление поста
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
