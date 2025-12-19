from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('contas.urls')),     
    path('admin/', admin.site.urls),
    path('carteira/', include('carteira.urls')),
    path('accounts/', include('allauth.urls')),
]
