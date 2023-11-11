from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # path('password/', views.password_user, name='password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="templates/users/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="templates/users/password_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="templates/users/password_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="templates/users/password_complete.html"), name="password_reset_complete"),
]

# PasswordResetView: apresenta um formulário para preencher o e-mail de recuperação. 
# Também gerará um link de uso único para a redefinição de senha e enviará esse link 
# para o endereço de e-mail que for preenchido, caso o mesmo exista na base de dados.

# PasswordResetDoneView: página mostrada depois que o usuário recebeu o link por e-mail para redifinir a senha.
# Entenda esse método como um template que irá mostrar que o e-mail foi enviado com sucesso.

# PasswordResetConfirmView: apresenta um formulário para inserir uma nova senha. 
# Esse método possui algumas caracteristicas especiais, como o argumento uidb64 e o token. 
# O token será para identificar se é uma senha válida conforme os padrões de segurança, já o uidb64 é o id do usuário codificado na base 64.

# PasswordResetCompleteView: exibe ao usuário um template informando que a senha foi alterada com sucesso