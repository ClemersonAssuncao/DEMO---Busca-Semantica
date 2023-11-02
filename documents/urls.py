from django.urls import path
from . import views

app_name = "documents"
urlpatterns = [
    path('', views.document_list, name='list'),
    path('add/', views.document_add_edit, name='add'),
    path('edit/<int:pk>', views.document_add_edit, name='edit'),
    path('folder/', views.folder_add_edit, name='add_folder'),
    path('folder/<int:pk>', views.folder_add_edit, name='edit_folder'),
    # path('register/', views.material_add, name='material_add'),
    # path('list/', views.material_list, name='material_list'),
    # path('register/', views.material_register, { 'pk': None}, name='material_register'),
]