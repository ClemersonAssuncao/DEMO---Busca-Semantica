from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_index, name='search_index'),
]