from __future__ import annotations
from django.contrib.contenttypes.models import ContentType
from carteira.models import Operacao, Acao, FII, Opcao, Posicao

from django.contrib.auth.models import User
from django.utils.timezone import localdate as date_today

# Repositorio de Operacaos
class OperacaoRepository:
    model_map = {"Acao": Acao, "FII": FII, "Opcao": Opcao}

    @staticmethod
    def save(dados_form, usuario):
        """
        Salva uma operação no banco a partir dos dados validados do formulário.
        :param dados_form: dict, dados validados do form (cleaned_data)
        :param usuario: User
        :return: Operacao
        """
        ativo_str = dados_form.pop("ativo")  # remove 'ativo' do dict
        tipo_model, obj_id = ativo_str.split(":")
        obj_id = int(obj_id)

        model = OperacaoRepository.model_map[tipo_model]
        ativo = model.objects.get(id=obj_id)

        # Cria instância do modelo Operacao
        operacao = Operacao(**dados_form)
        operacao.usuario = usuario
        operacao.content_type = ContentType.objects.get_for_model(model)
        operacao.object_id = ativo.id

        operacao.save()
        return operacao
    
    @staticmethod
    def finalizar_posicao(posicao:Posicao, usuario:User) -> bool:
        """
        Finaliza todas as operações associadas a uma posição, definindo sua quantidade como zero.
        :param posicao: Posicao
        :param usuario: User
        :return: None
        """
        operacao = Operacao.objects.create(
            usuario=usuario,
            ativo=posicao.ativo,
            quantidade=posicao.quantidade,
            preco=0,
            data=date_today(),
            tipo="VENDA" if posicao.quantidade > 0 else "COMPRA",
        )

        if operacao:
            return True
        return False

    @staticmethod
    def get_operacoes(usuario):
        """
        Retorna as operacoes do usuario
        :param usuario: User
        :return: QuerySet
        """
        return Operacao.objects.filter(usuario=usuario).order_by('-data')

    @staticmethod
    def get_operacao(usuario, ativo):
        """
        Retorna a operacao do usuario
        :param usuario: User
        :param ativo: Ativo
        :return: QuerySet
        """
        return Operacao.objects.filter(usuario=usuario, ativo=ativo)


class AcaoRepository:
    @staticmethod
    def get_acoes():
        """
        Retorna as acoes do usuario
        :return: QuerySet
        """
        return Acao.objects.all()

    @staticmethod
    def get_acao(codigo):
        """
        Retorna a acao do usuario
        :param codigo: str
        :return: QuerySet
        """
        return Acao.objects.filter(codigo=codigo)

    @staticmethod
    def save(dados_form):
        """
        Salva uma acao no banco a partir dos dados validados do formulário.
        :param dados_form: dict, dados validados do form (cleaned_data)
        :return: Acao
        """
        acao = Acao(**dados_form)
        acao.save()
        return acao


class FIIRepository:
    @staticmethod
    def get_fii_all():
        """
        Retorna o fii do usuario
        :return: QuerySet
        """
        return FII.objects.all()

    @staticmethod
    def get_fii(codigo):
        """
        Retorna o fii do usuario
        :param codigo: str
        :return: QuerySet
        """
        return FII.objects.filter(codigo=codigo)

    @staticmethod
    def save(dados_form):
        """
        Salva um fii no banco a partir dos dados validados do formulário.
        :param dados_form: dict, dados validados do form (cleaned_data)
        :return: FII
        """
        fii = FII(**dados_form)
        fii.save()
        return fii

class OpcaoRepository:
    @staticmethod
    def get_opcao_all():
        """
        Retorna a opcao do usuario
        :return: QuerySet
        """
        return Opcao.objects.all()

    @staticmethod
    def get_opcao(codigo:str):
        """
        Retorna a opcao do usuario
        :param codigo: str
        :return: QuerySet
        """
        return Opcao.objects.filter(codigo=codigo)

    @staticmethod
    def save(dados_form):
        """
        Salva uma opcao no banco a partir dos dados validados do formulário.
        :param dados_form: dict, dados validados do form (cleaned_data)
        :return: Opcao
        """
        opcao = Opcao(**dados_form)
        opcao.save()
        return opcao

class PosicaoRepository:

    @staticmethod
    def get_posicao_all_open(usuario:User):
        """
        Retorna a posicao do usuario
        :return: QuerySet
        """
        return Posicao.objects.filter(usuario=usuario, quantidade__gt=0)

    @staticmethod
    def get_posicao(usuario, ativo):
        """
        Retorna a posicao do usuario
        :param usuario: User
        :param ativo: Ativo
        :return: QuerySet
        """
        return Posicao.objects.filter(usuario=usuario, ativo=ativo)

    @staticmethod
    def get_posicao_by_id(usuario:User, id:int) -> Posicao | None:
        """
        Retorna a posicao do usuario pelo id
        :param id: int
        :param usuario: User
        :return: Posicao | None
        """
        try:
            return Posicao.objects.get(id=id, usuario=usuario)
        except Posicao.DoesNotExist:
            return None

    @staticmethod
    def save(usuario, dados_form) -> Posicao:
        """
        Salva uma posicao no banco a partir dos dados validados do formulário.
        :param usuario: User
        :param dados_form: dict, dados validados do form (cleaned_data)
        :return: Posicao
        """
        posicao = Posicao(**dados_form)
        posicao.usuario = usuario
        posicao.save()
        return posicao
    
    @staticmethod
    def delete(posicao:Posicao) -> None:
        """
        Deleta uma posicao do banco.
        :param posicao: Posicao
        :return: None
        """
        posicao.delete()