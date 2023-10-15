from django.urls import path
from . import views

urlpatterns = [
    path('register/<int:pk>', views.material_register, name='material_register'),
    path('register/', views.material_register,{ 'pk': None}, name='material_register'),
    path('', views.material_list, name='material_list'),
    # path('register/', views.material_register, { 'pk': None}, name='material_register'),
]