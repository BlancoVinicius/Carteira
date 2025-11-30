from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AcaoForm, OperacaoForm, OpcaoForm
from carteira.repositories import OperacaoRepository, AcaoRepository, PosicaoRepository, OpcaoRepository
from carteira.service import DashboardService, PosicaoService, OperacaoService
# Create your views here.

@login_required
def create_acao(request):

    if request.method == "POST":
        form = AcaoForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            acao = AcaoRepository.save(form.cleaned_data)
            return redirect("carteira:dashboard")
    else:
        form = AcaoForm()

    return render(request, "carteira/acao_form.html", {"form": form})

@login_required
def create_opcao(request):

    if request.method == "POST":
        form = OpcaoForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            opcao = OpcaoRepository.save(form.cleaned_data)
            return redirect("carteira:dashboard")
    else:
        form = OpcaoForm()

    return render(request, "carteira/opcao_form.html", {"form": form})

@login_required
def create_operacao(request):
    if request.method == "POST":
        form = OperacaoService.construir_form(request.POST)
        if form.is_valid():
            operacao = OperacaoRepository.save(form.cleaned_data, request.user)
            return redirect("carteira:dashboard")  # redireciona após salvar
    else:
        form = OperacaoService.construir_form()

    return render(request, "carteira/operacao_form.html", {"form": form})

@login_required
def operacao_list(request):
    """Lista todas as operações do usuário logado."""
    operacoes = OperacaoRepository.get_operacoes(request.user)

    # Calcula o total de cada operação (quantidade * preço)
    for op in operacoes:
        op.total = op.quantidade * op.preco

    context = {
        "operacoes": operacoes,
    }
    return render(request, "carteira/operacoes_list.html", context)

@login_required
def dashboard(request):
    context = DashboardService.get_resumo_carteira(request)

    if not context:
        return render(request, "carteira/dashboard.html", {"posicoes": []})

    return render(request, "carteira/dashboard.html", context)

@login_required
def posicoes_list(request):
    """Lista todas as posições do usuário logado."""
    posicoes = PosicaoRepository.abertas(request.user)

    for p in posicoes:
        p.lucro = p.valor_atual - (p.quantidade * p.preco_medio)
        p.rendimento = (p.lucro / (p.quantidade * p.preco_medio)) * 100 if p.quantidade * p.preco_medio != 0 else 0

    context = {
        "posicoes": posicoes,
    }
    return render(request, "carteira/posicoes.html", context)

@login_required
def fechar_posicao(request, id):
    form = PosicaoService.finish_posicao(request, id)
    return render(request, "carteira/operacao_form.html", {"form": form})