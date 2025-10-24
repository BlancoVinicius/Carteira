from django import forms
from carteira.models import Acao, Operacao, FII, Opcao
from django.contrib.contenttypes.models import ContentType


class AcaoForm(forms.ModelForm):
    # Sobrescrevendo campos do Model
    codigo = forms.ChoiceField(label="Código da Ação")

    class Meta:
        model = Acao
        fields = ["codigo", "setor", "descricao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # lista de códigos válidos
        lista_codigos = ["PETR4", "VALE3", "ITUB4", "BBDC3"]

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
        if Acao.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError(f"A ação '{codigo}' já está cadastrada.")

        return codigo


class OperacaoForm(forms.ModelForm):
    ativo = forms.ChoiceField(label="Ativo")

    class Meta:
        model = Operacao
        exclude = ["content_type", "object_id", "usuario"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.0001"}
            ),
            "preco": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.000001"}
            ),
            "corretagem": forms.NumberInput(attrs={"class": "form-control"}),
            "emolumentos": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Monta as opções de ativos (tuplas: (identificador, nome exibido))
        opcoes = []

        for acao in Acao.objects.all():
            opcoes.append((f"Acao:{acao.id}", f"Ação - {acao}"))
        for fii in FII.objects.all():
            opcoes.append((f"FII:{fii.id}", f"FII - {fii}"))
        for opcao in Opcao.objects.all():
            opcoes.append((f"Opcao:{opcao.id}", f"Opção - {opcao}"))

        self.fields["ativo"].choices = opcoes
        self.fields["ativo"].widget.attrs.update({"class": "form-select"})

    def save(self, usuario=None, commit=True):
        instance = super().save(commit=False)

        ativo_str = self.cleaned_data["ativo"]
        tipo_model, obj_id = ativo_str.split(":")
        obj_id = int(obj_id)

        # Mapeia o tipo de ativo para o modelo correspondente
        model_map = {"Acao": Acao, "FII": FII, "Opcao": Opcao}
        model = model_map[tipo_model]

        ativo = model.objects.get(id=obj_id)

        # Define content_type e object_id automaticamente
        instance.content_type = ContentType.objects.get_for_model(model)
        instance.object_id = ativo.id
        instance.usuario = usuario

        if commit:
            instance.save()
        return instance

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

# def clean_codigo(self):
#     """Valida se o código da ação já existe no banco."""
#     codigo = self.cleaned_data.get("codigo")

#     if not codigo:
#         raise forms.ValidationError("Selecione um código válido.")

#     # verifica se já existe alguma ação com esse código
#     if Acao.objects.filter(codigo=codigo).exists():
#         raise forms.ValidationError(f"A ação '{codigo}' já está cadastrada.")

#     return codigo
