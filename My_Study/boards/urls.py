from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
        path('<int:board_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
        path('<int:board_pk>/comments/', views.comment_create, name='comment_create'),
        path('<int:board_pk>/edit/', views.update, name='update'),
        path('<int:board_pk>/delete/', views.delete, name='delete'),
        path('<int:board_pk>/', views.detail, name='detail'),
        path('create/', views.create, name='create'),
        path('', views.list, name='list'),
    ]