from django.urls import path
# views.py에서 만든 함수를 씀!
from . import views

urlpatterns = [
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/', views.read, name='read'),
    path('', views.index, name='index'),
    ]