

    # Transformando a lista em string separada por espaços
from typing import Union, List
import yfinance as yf

class DadosMercado:
    
    def historico(self, ticker: Union[str, List[str]]) -> dict:
        # Garantir que temos uma lista
        if isinstance(ticker, str):
            lista_tickers = [ticker]
        else:
            lista_tickers = ticker

        # Criando objeto Tickers
        tickers_br = yf.Tickers(" ".join(lista_tickers))

        # Pegando preços de fechamento do último dia
        precos = {}
        for t in tickers_br.tickers:
            df = tickers_br.tickers[t].history(period='1d')
            precos[t] = df['Close'].iloc[-1]

        return precos


    # Baixando histórico de todos
    # dados_br = tickers_br.download(period='1mo', interval='1d')
    # print(dados_br)


    # vale3 = tickers_br.tickers['VALE3.SA']
    # print(vale3.history(period='1mo'))

# lista_br = ["PETR4.SA", "VALE3.SA", "ABEV3.SA"]

