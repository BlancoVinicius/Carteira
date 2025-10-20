from django.contrib import admin
from .models import Acao, Opcao, FII, Operacao, Posicao


@admin.register(Acao)
class AcaoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "setor")


@admin.register(Opcao)
class OpcaoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "tipo_opcao", "strike", "vencimento")


@admin.register(FII)
class FIIAdmin(admin.ModelAdmin):
    list_display = ("codigo", "segmento")


@admin.register(Operacao)
class OperacaoAdmin(admin.ModelAdmin):
    list_display = ("data", "tipo", "ativo", "quantidade", "preco", "usuario")


@admin.register(Posicao)
class PosicaoAdmin(admin.ModelAdmin):
    list_display = ("ativo", "quantidade", "preco_medio")
