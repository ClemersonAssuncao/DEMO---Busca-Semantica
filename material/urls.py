from django.urls import path
from . import views

urlpatterns = [
    path('register/<int:pk>', views.material_edit, name='material_edit'),
    path('register/', views.material_add, name='material_add'),
    path('', views.material_list, name='material_list'),
    # path('register/', views.material_register, { 'pk': None}, name='material_register'),
]