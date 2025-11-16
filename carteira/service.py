
from re import S
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login, logout

    # Transformando a lista em string separada por espaços
from typing import Union, List
import yfinance as yf

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



class LoginService:
    
    @staticmethod
    def login_user(request: HttpRequest ) -> bool:
        
        if request.method != "POST":
            return False

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return True
        else:
            return False




if __name__=="__main__":
    lista_br = ["PETR4", "VALE3", "ABEV3"]
    d = DadosMercado.historico(lista_br)