from django.shortcuts import render, redirect

from .forms import AcaoForm, OperacaoForm
from carteira.repositories import OperacaoRepository, AcaoRepository, PosicaoRepository
from carteira.service import DashboardService, LoginService
from django.conf import settings
# Create your views here.
def index(request):
    return render(request, "carteira/index.html")


def login(request):
    
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if LoginService.login_user(request):
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "carteira/login.html")

def register(request):
    return render(request, "carteira/register.html")

def logout(request):
    if request.user.is_authenticated:
        LoginService.logout_user(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

def create_acao(request):

    if request.method == "POST":
        form = AcaoForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            acao = AcaoRepository.save(form.cleaned_data)
            return redirect("carteira:index")  # redireciona após salvar
    else:
        form = AcaoForm()

    return render(request, "carteira/acao_form.html", {"form": form})


def create_operacao(request):
    if request.method == "POST":
        form = OperacaoForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            operacao = OperacaoRepository.save(form.cleaned_data, request.user)
            return redirect("carteira:dashboard")  # redireciona após salvar
    else:
        form = OperacaoForm()
        
    return render(request, "carteira/operacao_form.html", {"form": form})


def operacao_list(request):
    """Lista todas as operações do usuário logado."""
    operacoes = OperacaoRepository.get_operacoes(request.user).order_by('-data')

    # Calcula o total de cada operação (quantidade * preço)
    for op in operacoes:
        op.total = op.quantidade * op.preco

    context = {
        "operacoes": operacoes,
    }
    return render(request, "carteira/operacoes_list.html", context)


def dashboard(request):
    context = DashboardService.get_resumo_carteira(request)

    if not context:
        return render(request, "carteira/dashboard.html", {"posicoes": []})

    return render(request, "carteira/dashboard.html", context)

def posicoes_list(request):
    """Lista todas as posições do usuário logado."""
    posicoes = PosicaoRepository.get_posicao_all(request.user)

    for p in posicoes:
        p.lucro = p.valor_atual - (p.quantidade * p.preco_medio)
        p.rendimento = (p.lucro / (p.quantidade * p.preco_medio)) * 100 if p.quantidade * p.preco_medio != 0 else 0

    context = {
        "posicoes": posicoes,
    }
    return render(request, "carteira/posicoes2.html", context)