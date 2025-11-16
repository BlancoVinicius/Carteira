from django.shortcuts import render, redirect
from .forms import AcaoForm, OperacaoForm
from carteira.service import DadosMercado
from carteira.models import Posicao
from django.http import JsonResponse

from carteira.service import LoginService
# Create your views here.
def index(request):
    return render(request, "carteira/index.html")


def login(request):
    if LoginService.login_user(request):
        return redirect("carteira:dashboard")
    
    return render(request, "carteira/login.html")


def register(request):
    return render(request, "carteira/register.html")


def create_acao(request):

    if request.method == "POST":
        form = AcaoForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            form.save(request.user)
            return redirect("carteira:index")  # redireciona após salvar
    else:
        form = AcaoForm()

    return render(request, "carteira/acao_form.html", {"form": form})


def create_operacao(request):
    if request.method == "POST":
        form = OperacaoForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            form.save(usuario=request.user)
            return redirect("carteira:index")  # redireciona após salvar
    else:
        form = OperacaoForm()
        
    return render(request, "carteira/operacao_form.html", {"form": form})


def dashboard(request):
    posicoes = Posicao.objects.all()
    lista_tickers = []
    dados = {}
    for posicao in posicoes:
        lista_tickers.append(posicao.ativo.codigo)

    df = DadosMercado.historico(lista_tickers)
    
    for posicao in posicoes:
        dados[posicao.ativo.codigo] = {
            "quantidade": f"{posicao.quantidade:.0f}",
            "preco_medio": f"{posicao.preco_medio:.2f}",
            "cotacao":f"{df[posicao.ativo.codigo + ".SA"]:.2f}",
        }

    # return JsonResponse(dados)
    return render(request, "carteira/dashboard.html", {"dados": dados})
