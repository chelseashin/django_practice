from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/delete/', views.delete, name="delete"),
    path('create/', views.create, name="create"), 
    path('', views.index, name='index'),
    ]