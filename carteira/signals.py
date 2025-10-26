from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db import models
from .models import Operacao, Posicao
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal

@receiver(post_save, sender=Operacao)
def update_saldo(sender, instance, **kwargs):
    
    content_type = instance.content_type
    # content_type = ContentType.objects.get_for_model(instance)

    ops = Operacao.objects.filter(content_type=content_type, object_id=instance.object_id)

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
    posicao.save()

# @receiver(post_save, sender=Operacao)
# def update_saldo(sender, instance, **kwargs):
    
#     content_type = ContentType.objects.get_for_model(instance.ativo)

#     ops = Operacao.objects.filter(content_type=content_type, object_id=instance.ativo.id)

#     quantidade =  Decimal(0)
#     preco_medio = Decimal(0)
        
#     for op in ops:
#         if op.tipo == 'COMPRA':
#             quantidade += op.quantidade
#             preco_medio += op.valor_atual    

#         elif op.tipo == 'VENDA':
#             quantidade -= op.quantidade
#             preco_medio -= op.valor_atual
    
#     preco_medio = preco_medio / quantidade

#     posicao, created = Posicao.objects.get_or_create(content_type=content_type, object_id=instance.ativo.id)
#     posicao.quantidade = quantidade
#     posicao.preco_medio = preco_medio
#     posicao.save()