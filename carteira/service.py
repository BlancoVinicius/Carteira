from uu import Error
from carteira.repositories import PosicaoRepository, AcaoRepository, FIIRepository, OpcaoRepository, OperacaoRepository
from decimal import Decimal, ROUND_DOWN

    # Transformando a lista em string separada por espaços
from typing import Union, List
import yfinance as yf
from carteira.forms import OperacaoForm
from django.utils.timezone import localdate as date_today
from django.http import QueryDict
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model

USER = get_user_model()

class DadosMercado:
    
    def historico(ticker: Union[str, List[str]]) -> dict:
        # Garantir que temos uma lista
        lista_tickers = DadosMercado._normalizar_ticker(ticker)

        # Criando objeto Tickers
        tickers_br = yf.Tickers(" ".join(lista_tickers))

        # Pegando preços de fechamento do último dia
        precos = {}
        for t in tickers_br.tickers:
            df = tickers_br.tickers[t].history(period='1d')
            precos[t] = df['Close'].iloc[-1]
        
        return precos

    def _normalizar_ticker(ticker: Union[str, List[str]]) -> Union[str, List[str]]:
        
        if isinstance(ticker, str):
            if not ticker.endswith(".SA"):
                ticker += ".SA"
                return ticker
            else:
                return ticker
        else:
            lista_tickers = [t + ".SA" if not t.endswith(".SA") else t for t in ticker]
            return lista_tickers


class DashboardService:
    
    def get_resumo_carteira(request):
        posicoes = PosicaoRepository.abertas(request.user)

        if not posicoes:
            return {"posicoes": []}

        from carteira.models import Acao
        
        lista_tickers = [p.ativo.codigo for p in posicoes if isinstance(p.ativo, Acao)]

        df = DadosMercado.historico(lista_tickers)

        def to_decimal(valor):
            """Converte para Decimal com 2 casas e ROUND_HALF_UP."""
            return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        # Cálculos agregados
        valor_investido = sum(p.quantidade * p.preco_medio for p in posicoes)
        valor_investido = valor_investido.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        valor_atual = sum(
            p.quantidade * to_decimal(df[p.ativo.codigo + ".SA"]) for p in posicoes if isinstance(p.ativo, Acao)
        )
        valor_atual = Decimal(valor_atual).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        lucro = (valor_atual - valor_investido).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        percentual = (lucro / valor_investido * 100).quantize(Decimal("0.01"), rounding=ROUND_DOWN) if valor_investido > 0 else Decimal("0.00")

        # Atualiza cada posição
        for p in posicoes:
            preco_atual = to_decimal(df[p.ativo.codigo + ".SA"]) if isinstance(p.ativo, Acao) else Decimal("0.00")
            p.preco_atual = preco_atual

            p.lucro = (p.quantidade * (preco_atual - p.preco_medio)).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

            base = p.quantidade * p.preco_medio
            p.percentual = ((p.lucro / base) * 100).quantize(Decimal("0.01"), rounding=ROUND_DOWN) if base > 0 else Decimal("0.00")

        resumo = {
            "valor_investido": valor_investido,
            "valor_atual": valor_atual,
            "lucro": lucro,
            "percentual": percentual,
        }

        context = {
            "resumo": resumo,
            "posicoes": posicoes,
        }
        return context

class PosicaoService:
    
    @staticmethod
    def finish_posicao(request, id):
        """
        Finaliza uma posicao, definindo sua quantidade como zero.
        :param posicao: Posicao
        :return: None
        """
        # posicao = PosicaoRepository.get_posicao_by_id(request.user, id)

        # if posicao:
        #     return OperacaoRepository.finalizar_posicao(posicao, request.user)
        # return False 
        form = OperacaoService.construir_form_zerar_posicao(request.user, id)
        return form
    
    @staticmethod
    def buscar_posicoes_usuario(user:USER):
        return PosicaoRepository.abertas(user)


class OperacaoService:

    @staticmethod
    def construir_form(data:QueryDict | None = None) -> OperacaoForm:
        opcoes = []

        for acao in AcaoRepository.get_acoes():
            opcoes.append((f"{ContentType.objects.get_for_model(acao).id}:{acao.id}", f"{acao}"))
        for fii in FIIRepository.get_fii_all():
            opcoes.append((f"{ContentType.objects.get_for_model(fii).id}:{fii.id}", f"{fii}"))
        for opcao in OpcaoRepository.get_opcao_all():
            opcoes.append((f"{ContentType.objects.get_for_model(opcao).id}:{opcao.id}", f"{opcao}"))

        op_form = OperacaoForm(data)
        op_form.set_ativo(opcoes)

        return op_form    

    @staticmethod
    def construir_form_zerar_posicao(usuario, id):
        posicao = PosicaoRepository.get_posicao_by_id(usuario, id)

        form = OperacaoForm(initial={
            "quantidade": posicao.quantidade if posicao.quantidade > 0 else posicao.quantidade * (-1),
            "tipo": "VENDA" if posicao.quantidade > 0 else "COMPRA",
            "data": date_today(),     # se tiver campo data
        })

        form.set_ativo([(f"{ContentType.objects.get_for_model(posicao.ativo).id}:{posicao.ativo.id}", f"{posicao.ativo}")])
        return form

    @staticmethod
    def salvar_operacao(dados_form: dict, usuario: USER):
        """
        Salva uma operação no banco a partir dos dados validados do formulário.
        :param dados_form: dict, dados validados do form (cleaned_data)
        :param usuario: User
        :return: Operacao
        """
        ativo_str = dados_form.pop("ativo")  # remove 'ativo' do dict
        tipo_model_id, obj_id = ativo_str.split(":")
        obj_id = int(obj_id)
        tipo_model_id = int(tipo_model_id)

        content_type = ContentType.objects.get_for_id(tipo_model_id)
        if not content_type.app_label == "carteira":
            raise Error("DADOS NÂO CONFEREM!")

        return OperacaoRepository.save(dados_form, usuario, content_type, obj_id)
        
    @staticmethod
    def buscar_operacoes_pelo_usuario(user:USER):
        return OperacaoRepository.get_operacoes(user)

class AcaoService:

    @staticmethod
    def save(dados_form: dict):
        return AcaoRepository.save(dados_form)


class OpcaoService:

    @staticmethod
    def save(dados_form: dict):
        return OpcaoRepository.save(dados_form)