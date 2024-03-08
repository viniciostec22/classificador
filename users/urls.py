from django.urls import path
from . import views


urlpatterns = [
   path('new_user/', views.new_user, name="cadastro" ),
   path('login/', views.logar, name="login"),
   path('logout/', views.logout, name='logout')
]