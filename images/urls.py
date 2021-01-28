from django.urls import path

from . import views


urlpatterns = [
    path('', views.ImageListView.as_view(), name='index'),
    path('upload/', views.ImageCreateView.as_view(), name='upload'),
    path('update/<int:pk>/', views.ImageResizeView.as_view(), name='update'),
]
