from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PerfilUsuario, SaldoCriptomoedas
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from decimal import Decimal, InvalidOperation
from django.db import transaction
import json

# Views de renderização simples
def cadastro_view(request):
    return render(request, 'cadastro.html')

# View para usuários não logados
def pagina_inicial(request):
    # Se o usuário estiver logado, redirecione para a página inicial específica
    if request.user.is_authenticated:
        return redirect('pagina_inicial_logado')
    
    return render(request, 'home.html')  # Template para usuários não logados

# View para usuários logados
@login_required
def pagina_inicial_logado(request):
    return render(request, 'home2.html')  # Template para usuários logados

def pagina_inicial_view(request):
    return render(request, 'home.html')

def deposito_view(request):
    return render(request, 'deposito.html')

# View de login
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']
        usuario = authenticate(request, username=email, password=senha)
        if usuario is not None:
            login(request, usuario)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('compra')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            return redirect('login')
    return render(request, 'login.html')

# View de registro de novo usuário
def registro_view(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        confirmar_senha = request.POST['confirmar-senha']

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return redirect('register')

        usuario = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
        usuario.save()
        login(request, usuario)
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('pagina_inicial')

    return render(request, 'cadastro.html')

# View de logout
def sair_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('login')

# View de exibição de dados da conta do usuário
@login_required
def conta_view(request):
    usuario = request.user
    perfil_usuario = request.user.perfilusuario
    saldos_criptomoedas = SaldoCriptomoedas.objects.filter(usuario=request.user)
    
    context = {
        'usuario': usuario,
        'saldo_usuario': perfil_usuario.saldo_carteira,
        'saldos_criptomoedas': saldos_criptomoedas,
        'nome_completo_usuario': f"{usuario.first_name} {usuario.last_name}",
        'email_usuario': usuario.email,
    }
    return render(request, 'minha_conta.html', context)

# View da carteira do usuário
@login_required
def carteira_view(request):
    perfil_usuario = request.user.perfilusuario
    saldos_criptomoedas = SaldoCriptomoedas.objects.filter(usuario=request.user)
    
    context = {
        'saldo_usuario': perfil_usuario.saldo_carteira,
        'saldos_criptomoedas': saldos_criptomoedas,
    }
    return render(request, 'carteira.html', context)

# View para a página de compra
@login_required
def compra_view(request):
    perfil_usuario = request.user.perfilusuario
    
    context = {
        'saldo_usuario': perfil_usuario.saldo_carteira,
    }
    return render(request, 'compra.html', context)

# View para processar a compra de criptomoedas
@require_POST
@csrf_protect
@login_required
def processar_compra(request):
    try:
        # Validar e converter os valores recebidos
        valor_brl = request.POST.get('valor_brl')
        cripto = request.POST.get('cripto')
        quantidade_cripto = request.POST.get('quantidade_cripto')

        # Checar se os valores são válidos
        if not valor_brl or not quantidade_cripto or not cripto:
            return JsonResponse({'error': 'Todos os campos são obrigatórios.'}, status=400)

        try:
            valor_brl = Decimal(valor_brl)
            quantidade_cripto = Decimal(quantidade_cripto)
        except InvalidOperation:
            return JsonResponse({'error': 'Valores fornecidos são inválidos.'}, status=400)

        perfil_usuario = request.user.perfilusuario

        if valor_brl <= 0:
            return JsonResponse({'error': 'Valor inválido para compra.'}, status=400)

        if valor_brl > perfil_usuario.saldo_carteira:
            return JsonResponse({'error': 'Saldo insuficiente.'}, status=400)

        # Processamento da compra
        perfil_usuario.saldo_carteira -= valor_brl
        perfil_usuario.save()

        # Atualizar ou criar saldo de criptomoeda
        saldo_cripto, created = SaldoCriptomoedas.objects.get_or_create(
            usuario=request.user,
            nome=cripto,
            defaults={'simbolo': cripto, 'quantidade': 0}
        )
        saldo_cripto.quantidade += quantidade_cripto
        saldo_cripto.save()

        # Buscar todas as criptomoedas do usuário
        saldos_criptomoedas = SaldoCriptomoedas.objects.filter(usuario=request.user)
        lista_criptos = [
            {
                'nome': c.nome,
                'simbolo': c.simbolo,
                'quantidade': float(c.quantidade)
            } for c in saldos_criptomoedas
        ]

        return JsonResponse({
            'success': True,
            'saldo_atual': float(perfil_usuario.saldo_carteira),
            'cripto_comprada': {
                'nome': cripto,
                'simbolo': saldo_cripto.simbolo,
                'quantidade': float(saldo_cripto.quantidade)
            },
            'saldos_criptomoedas': lista_criptos
        })

    except (ValueError, TypeError) as e:
        return JsonResponse({'error': f'Dados inválidos fornecidos: {str(e)}'}, status=400)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao processar a compra: {str(e)}")
        return JsonResponse({'error': 'Erro interno do servidor.'}, status=500)
# View para atualizar o saldo do usuário
@require_POST
@csrf_protect
@login_required
def atualizar_saldo(request):
    try:
        data = json.loads(request.body)
        valor_str = data.get('valor', '0')

        try:
            valor = Decimal(valor_str)
        except InvalidOperation:
            return JsonResponse({'sucesso': False, 'erro': 'Valor inválido'}, status=400)

        if valor <= 0:
            return JsonResponse({'sucesso': False, 'erro': 'O valor deve ser positivo'}, status=400)

        with transaction.atomic():
            perfil_usuario = request.user.perfilusuario
            perfil_usuario.saldo_carteira += valor
            perfil_usuario.saldo_total += valor
            perfil_usuario.save()

        return JsonResponse({
            'sucesso': True,
            'novo_saldo_carteira': float(perfil_usuario.saldo_carteira),
            'novo_saldo_total': float(perfil_usuario.saldo_total)
        })
    except json.JSONDecodeError:
        return JsonResponse({'sucesso': False, 'erro': 'Dados JSON inválidos'}, status=400)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao atualizar saldo: {str(e)}")
        return JsonResponse({'sucesso': False, 'erro': 'Erro interno do servidor'}, status=500)
# View para atualizar dados do usuário
@login_required
def atualizar_dados(request):
    if request.method == 'POST':
        usuario = request.user
        primeiro_nome = request.POST.get('primeiro_nome', '').strip()
        sobrenome = request.POST.get('sobrenome', '').strip()
        email = request.POST.get('email', '').strip()

        # Garantir que o campo "Primeiro Nome" não esteja vazio
        if not primeiro_nome:
            messages.error(request, 'O campo "Primeiro Nome" é obrigatório.')
            return redirect('conta')

        # Se o sobrenome estiver vazio, atribui um valor padrão
        if not sobrenome:
            sobrenome = 'N/A'

        # Verifica se o novo e-mail já está sendo usado por outro usuário
        if User.objects.filter(username=email).exclude(id=usuario.id).exists():
            messages.error(request, 'O e-mail já está sendo usado por outro usuário.')
            return redirect('conta')

        # Atualizando os campos do usuário
        usuario.first_name = primeiro_nome
        usuario.last_name = sobrenome
        usuario.email = email
        usuario.username = email  # Garante que o username seja igual ao email

        # Salvando as mudanças no banco de dados
        try:
            usuario.save()
            messages.success(request, 'Dados atualizados com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar os dados: {str(e)}')

        return redirect('conta')
    else:
        perfil_usuario = request.user.perfilusuario
        context = {
            'saldo_usuario': perfil_usuario.saldo_carteira,
            'nome_completo_usuario': f"{request.user.first_name} {request.user.last_name}",
            'email_usuario': request.user.email,
        }
        return render(request, 'conta.html', context)

# View para obter o saldo do usuário (utilizada via AJAX)
@login_required
def obter_saldo(request):
    perfil_usuario = request.user.perfilusuario
    return JsonResponse({'saldo': float(perfil_usuario.saldo_carteira)})