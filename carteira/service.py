from carteira.repositories import PosicaoRepository, OperacaoRepository
from decimal import Decimal, ROUND_DOWN

    # Transformando a lista em string separada por espaços
from typing import Union, List
import yfinance as yf
from carteira.forms import OperacaoForm
from django.utils.timezone import localdate as date_today

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
        posicoes = PosicaoRepository.get_posicao_all_open(request.user)

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
        valor_atual = valor_atual.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

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
        posicao = PosicaoRepository.get_posicao_by_id(request.user, id)

        if posicao:
            return OperacaoRepository.finalizar_posicao(posicao, request.user)
        return False 

    @staticmethod
    def teste_posicao_form_transition(request, id) -> OperacaoForm:
        
        posicao = PosicaoRepository.get_posicao_by_id(request.user, id)

        form = OperacaoForm(initial={
            "ativo": posicao.ativo.id,         # se for ModelChoiceField precisa ser o ID
            "quantidade": posicao.quantidade,
            "tipo": "VENDA",
            "data": date_today(),     # se tiver campo data
        })

        return form