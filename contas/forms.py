from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nome de usuário"
        })
        
        self.fields["email"].label = "E-mail"
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Digite seu e-mail"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Senha"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirme a senha"
        })
