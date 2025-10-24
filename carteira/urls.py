from django.contrib import admin
from django.urls import path
from . import views

app_name = "carteira"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("criar_acao/", views.create_acao, name="create_acao"),
    path("criar_operacao/", views.create_operacao, name="create_operacao"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
