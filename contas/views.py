from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from contas.service import LoginService
from django.conf import settings
from django.contrib.auth import login

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("carteira:dashboard")
    return render(request, "contas/index.html")

# def login(request):
#     if request.user.is_authenticated:
#         return redirect(settings.LOGIN_REDIRECT_URL)

#     if LoginService.login_user(request):
#         return redirect(settings.LOGIN_REDIRECT_URL)
#     return render(request, "contas/login.html")

# def register(request):
#     # if request.method == "POST":
#     #     form = UserRegisterForm(request.POST)
#     #     if form.is_valid():
#     #         user = form.save()
#     #         login(request, user)
#     #         return redirect("carteira:dashboard")
#     #     else:
#     #         print("ERROS DO FORM:", form.errors) 
#     # else:
#     #     form = UserRegisterForm()

#     return render(request, "contas/register.html")
#     return render(request, "contas/register.html", {"form": form})

# @login_required
# def logout(request):
#     if request.user.is_authenticated:
#         LoginService.logout_user(request)
#     return redirect(settings.LOGOUT_REDIRECT_URL)










