"""
URL configuration for BuscaSemantica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about, name='index'),
    path('controll/', views.controll, name='controll'),
    path('documents/', include('documents.urls'), name='documents'),
    path('', include('search.urls'), name='search'),
    path('user/', include('users.urls'), name='users'),
    
    path('reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_confirm.html", success_url= "/user/reset_password_complete/", ), name="password_reset_confirm"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
