from carteira.models import Acao, Operacao, Opcao
from django import forms
from typing import List

from carteira.repositories import AcaoRepository, OpcaoRepository, EstrategiaRepository, EstrategiaExecutadaRepository

class AcaoForm(forms.ModelForm):
    # Sobrescrevendo campos do Model
    # codigo = forms.ChoiceField(label="Código da Ação")

    codigo = forms.CharField(
        label="Código da Ação",
        widget=forms.TextInput(attrs={"class": "form-control", "list": "lista_codigos"}),
    )

    class Meta:
        model = Acao
        fields = ["codigo", "setor", "descricao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # lista de códigos válidos
        lista_codigos = ["PETR4", "VALE3", "ITUB4", "BBDC3"]
        self.lista_codigos = lista_codigos
        
        # gera a lista de opções para o <select>
        self.fields["codigo"].choices = [(c, c) for c in lista_codigos]
        self.fields["codigo"].choices.insert(0, ("", "Selecione um código"))

        # Aplica classe Bootstrap
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_codigo(self):
        """Valida se o código da ação já existe no banco."""
        codigo = self.cleaned_data.get("codigo")

        if not codigo:
            raise forms.ValidationError("Selecione um código válido.")

        # verifica se já existe alguma ação com esse código
        if  AcaoRepository.get_acao(codigo=codigo).exists():
            raise forms.ValidationError(f"A ação '{codigo}' já está cadastrada.")

        return codigo


class OperacaoForm(forms.ModelForm):
    selecionar_ativo = forms.ChoiceField(label="Ativo")
    
    radio_buton = forms.ChoiceField(
    label="Selecione uma opção",
    choices=[
        ("NOVA", "Nova estratégia"),
        ("EXISTENTE", "Estratégia existente"),
    ],
    widget=forms.RadioSelect)
    # estrategia = forms.ChoiceField(label="Selecione uma Estratégia", required=False, widget=forms.Select(attrs={"class": "form-select"}))
    # estrategia_existente = forms.ChoiceField(label="Selecione Estratégia em andamento", required=False, widget=forms.Select(attrs={"class": "form-select"}))
    estrategia_executada = forms.ModelChoiceField(
        queryset=EstrategiaExecutadaRepository.get_all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Selecione uma Estratégia em andamento"
    )
    
    estrategia = forms.ModelChoiceField(
        queryset=EstrategiaRepository.get_all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Selecione uma Estratégia"
    )


    class Meta:
        model = Operacao
        fields = ["radio_buton", "estrategia", "estrategia_executada", "data", "tipo", "quantidade", "preco", "corretagem", "emolumentos", "selecionar_ativo"]
        #exclude = ["content_type", "object_id", "usuario"]
        widgets = {
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
            "estrategia": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "preco": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.000001"}
            ),
            "corretagem": forms.NumberInput(attrs={"class": "form-control"}),
            "emolumentos": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def set_ativo(self, ativos: List[tuple]):
        self.fields["selecionar_ativo"].choices = ativos
        self.fields["selecionar_ativo"].widget.attrs.update({"class": "form-select"})

    # def set_estrategia_executada(self, estrategia:EstrategiaExecutada):
    #     self.estrategia_executada = estrategia 

    def clean_quantidade(self):
        qtd = self.cleaned_data.get("quantidade")
    
        if qtd <= 0:
            raise forms.ValidationError("Quantidade deve ser maior que zero.")

        return qtd

    def clean_preco(self):
        preco = self.cleaned_data.get("preco")
    
        if preco <= 0:
            raise forms.ValidationError("Preço deve ser maior que zero.")

        return preco

    def clean_estrategia_executada(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("radio_buton")

        if tipo == "EXISTENTE":
            execucao = cleaned_data.get("estrategia_executada")
            if not execucao:
                raise forms.ValidationError("Selecione uma estratégia em andamento.")

        return execucao
    # def clean(self):
    #     cleaned_data = super().clean()
    #     tipo = cleaned_data.get("radio_buton")

    #     if tipo == "NOVA":
    #         estrategia_base = cleaned_data.get("estrategia")
    #         if not estrategia_base:
    #             raise forms.ValidationError("Selecione uma estratégia.")

    #     if tipo == "EXISTENTE":
    #         execucao = cleaned_data.get("estrategia_existente")
    #         if not execucao:
    #             raise forms.ValidationError("Selecione uma estratégia em andamento.")

    #     return cleaned_data



class OpcaoForm(forms.ModelForm):
    
    # codigo = forms.ChoiceField(label="Código da Ação")
    codigo = forms.CharField(
        label="Código da Opção",
        widget=forms.TextInput(attrs={"class": "form-control", "list": "lista_codigos"}),
    )

    class Meta:
        model = Opcao
        fields = ["codigo", "tipo_opcao", "descricao", "modelo", "strike", "vencimento"]
        widgets = {
            "vencimento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # lista de códigos válidos
        lista_codigos = ["PETRW200", "VALEX210", "ITUBL315", "BBDCX220"]
        self.lista_codigos = lista_codigos

        # gera a lista de opções para o <select>
        self.fields["codigo"].choices = [(c, c) for c in lista_codigos]
        self.fields["codigo"].choices.insert(0, ("", "Selecione um código"))

        # Aplica classe Bootstrap
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_codigo(self):
        """Valida se o código da ação já existe no banco."""
        codigo = self.cleaned_data.get("codigo")

        if not codigo:
            raise forms.ValidationError("Selecione um código válido.")

        # verifica se já existe alguma ação com esse código
        if  OpcaoRepository.get_opcao(codigo=codigo).exists():
            raise forms.ValidationError(f"A opção '{codigo}' já está cadastrada.")

        return codigo
    