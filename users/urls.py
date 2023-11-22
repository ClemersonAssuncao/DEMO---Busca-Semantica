from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(  template_name="users/password_reset.html", 
                                                success_url= "/user/reset_password_done/",
                                                email_template_name = "users/password_reset_email.html",
                                                subject_template_name= "users/password_reset_subject.txt",), 
                                                name="reset_password", ),

    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_done.html"), name="password_reset_done"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_complete.html"), name="password_reset_complete"),
]
