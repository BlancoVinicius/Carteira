from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest

class LoginService:
    
    @staticmethod
    def login_user(request: HttpRequest ) -> bool:
        
        if request.method != "POST":
            return False

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return True
        else:
            return False

    @staticmethod
    def logout_user(request: HttpRequest ) -> bool:
        logout(request)
        return True