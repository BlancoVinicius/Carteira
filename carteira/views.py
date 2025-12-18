from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AcaoForm, OpcaoForm
from carteira.service import DashboardService, OpcaoService, PosicaoService, OperacaoService, AcaoService
# Create your views here.

@login_required
def create_acao(request):

    if request.method == "POST":
        form = AcaoForm(request.POST)
        if form.is_valid():
            AcaoService.save(form.cleaned_data)
            return redirect("carteira:dashboard")
    else:
        form = AcaoForm()

    return render(request, "carteira/acao_form.html", {"form": form})

@login_required
def create_opcao(request):

    if request.method == "POST":
        form = OpcaoForm(request.POST)
        if form.is_valid():
            OpcaoService.save(form.cleaned_data)
            return redirect("carteira:dashboard")
    else:
        form = OpcaoForm()

    return render(request, "carteira/opcao_form.html", {"form": form})

@login_required
def create_operacao(request):
    if request.method == "POST":
        form = OperacaoService.construir_form(request.POST)
        if form.is_valid():
            OperacaoService.salvar_operacao(form.cleaned_data, request.user)
            return redirect("carteira:dashboard")  # redireciona após salvar
    else:
        form = OperacaoService.construir_form()

    return render(request, "carteira/operacao_form.html", {"form": form})

@login_required
def operacao_list(request):
    """Lista todas as operações do usuário logado."""
    operacoes = OperacaoService.buscar_operacoes_pelo_usuario(request.user)

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
    posicoes = PosicaoService.buscar_posicoes_usuario(request.user)

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