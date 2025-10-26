from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Operacao, Posicao
from decimal import Decimal

@receiver(post_save, sender=Operacao)
def update_saldo(sender, instance, **kwargs):
    
    content_type = instance.content_type
    # content_type = ContentType.objects.get_for_model(instance)

    ops = Operacao.objects.filter(content_type=content_type, object_id=instance.object_id, usuario=instance.usuario)

    quantidade =  Decimal(0)
    preco_medio = Decimal(0)
        
    for op in ops:
        if op.tipo == 'COMPRA':
            quantidade += op.quantidade
            preco_medio += op.valor_atual

        elif op.tipo == 'VENDA':
            quantidade -= op.quantidade
            preco_medio -= op.valor_atual
    
    preco_medio = preco_medio / quantidade

    posicao, created = Posicao.objects.get_or_create(content_type=content_type, object_id=instance.object_id)
    posicao.quantidade = quantidade
    posicao.preco_medio = preco_medio
    posicao.usuario = instance.usuario
    posicao.save()
