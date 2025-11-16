from django.urls import path
from . import views

app_name = "carteira"

urlpatterns = [
    path("criar_acao/", views.create_acao, name="create_acao"),
    path("criar_opcao/", views.create_opcao, name="create_opcao"),
    path("criar_operacao/", views.create_operacao, name="create_operacao"),
    path("operacao_list/", views.operacao_list, name="operacao_list"),
    path("posicoes/", views.posicoes_list, name="posicoes"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
