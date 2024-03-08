from django.urls import path
from . import views


urlpatterns = [
  path('new_images/', views.images, name='new_images'),
  path('galeria/', views.galeria, name='galeria'),
  path('dashboard/', views.dashboard, name="dashboard"),
  path('download/', views.download, name='download')
]