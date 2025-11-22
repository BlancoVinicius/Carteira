from django.db import models
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


User = get_user_model()


# -------------------------
# Classe base abstrata
# -------------------------
class AtivoBase(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descricao = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True

    def valor_atual(self):
        raise NotImplementedError("Subclasse deve implementar o método valor_atual()")

    def __str__(self):
        return self.codigo


# -------------------------
# Classes concretas
# -------------------------
class Acao(AtivoBase):
    setor = models.CharField(max_length=100, blank=True)

    def valor_atual(self) -> Decimal:
        return 0


class Opcao(AtivoBase):
    tipo_opcao = models.CharField(
        max_length=1, choices=[("C", "Call"), ("P", "Put")], default="C"
    )
    modelo = models.CharField(
        max_length=3,
        choices=[("AME", "Americana"), ("EUR", "Européia")],
        blank=False,
        null=False,
    )
    strike = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    vencimento = models.DateField(blank=False, null=False)

    class Meta:
        db_table = "opcoes"
        # unique_together = ("tipo", "strike", "vencimento", "codigo")

    def valor_atual(self) -> Decimal:
        return 0


class FII(AtivoBase):
    segmento = models.CharField(max_length=100, blank=True)

    def valor_atual(self) -> Decimal:
        return 0


# -------------------------
# Operações genéricas (usam GenericForeignKey)
# -------------------------
class Operacao(models.Model):
    TIPO = [("COMPRA", "Compra"), ("VENDA", "Venda")]

    # ContentType genérico para qualquer ativo
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    ativo = GenericForeignKey("content_type", "object_id")

    data = models.DateField()
    tipo = models.CharField(max_length=6, choices=TIPO)
    quantidade = models.DecimalField(max_digits=20, decimal_places=4)
    preco = models.DecimalField(max_digits=20, decimal_places=6)
    corretagem = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    emolumentos = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data", "-created_at"]

    def __str__(self):
        return f"{self.data} - {self.tipo} {self.quantidade} {self.ativo}"

    @property
    def custo_total(self):
        return (self.preco * self.quantidade) + self.corretagem + self.emolumentos

    @property
    def valor_atual(self):
        return self.quantidade * self.preco

# -------------------------
# Posições genéricas
# -------------------------
class Posicao(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    ativo = GenericForeignKey("content_type", "object_id")

    quantidade = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    preco_medio = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "posicao"
        verbose_name = "Posicao"
        verbose_name_plural = "Posicoes"
        unique_together = ("content_type", "object_id", "usuario")

    def __str__(self):
        return f"Posição {self.ativo}: {self.quantidade} @ {self.preco_medio}"

    @property
    def valor_atual(self):
        return self.quantidade * self.preco_medio

    