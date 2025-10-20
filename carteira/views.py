from django.shortcuts import render, redirect
from .forms import AcaoForm, OperacaoForm


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
            form.save()
            return redirect("carteira:index")  # redireciona após salvar
    else:
        form = AcaoForm()

    return render(request, "carteira/acao_form.html", {"form": form})


def create_operacao(request):
    if request.method == "POST":
        form = OperacaoForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            form.save()
            return redirect("carteira:index")  # redireciona após salvar
    else:
        form = OperacaoForm()

    return render(request, "carteira/operacao_form.html", {"form": form})
