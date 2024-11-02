"""
URL configuration for NEX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('carteira/', views.carteira_view, name='carteira'),
    path('compra/', views.compra_view, name='compra'),
    path('login/', views.login_view, name='login'),
    path('', views.pagina_inicial, name='pagina_inicial'),  # Página inicial para não logados
    path('inicio/', views.pagina_inicial_logado, name='pagina_inicial_logado'), 
    path('registro/', views.registro_view, name='registro'),
    path('sair/', views.sair_view, name='sair'),
    path('deposito/', views.deposito_view, name='deposito'),
    path('conta/', views.conta_view, name='conta'),
    path('obter_saldo/', views.obter_saldo, name='obter_saldo'),
    path('atualizar_saldo/', views.atualizar_saldo, name='atualizar_saldo'),
    path('processar_compra/', views.processar_compra, name='processar_compra'),
    path('atualizar_dados/', views.atualizar_dados, name='atualizar_dados'),
]
