from django.urls import path
from . import views

app_name = "carteira"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("criar_acao/", views.create_acao, name="create_acao"),
    path("criar_operacao/", views.create_operacao, name="create_operacao"),
    path("operacao_list/", views.operacao_list, name="operacao_list"),
    path("posicoes/", views.posicoes_list, name="posicoes"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
