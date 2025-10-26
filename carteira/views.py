from django.shortcuts import render, redirect

from .forms import AcaoForm, OperacaoForm
from carteira.repositories import OperacaoRepository, AcaoRepository
from carteira.service import DashboardService

# Create your views here.
def index(request):
    return render(request, "carteira/index.html")


def login(request):
    return render(request, "carteira/login.html")


def register(request):
    return render(request, "carteira/register.html")


def create_acao(request):

    if request.method == "POST":
        form = AcaoForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            acao = AcaoRepository.save(form.cleaned_data, request.user)
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