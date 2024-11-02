from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import PerfilUsuario, SaldoCriptomoedas

class SaldoCriptomoedasInline(admin.TabularInline):
    model = SaldoCriptomoedas
    extra = 0
    can_delete = False
    readonly_fields = ('nome', 'simbolo', 'quantidade', 'criado_em', 'atualizado_em')  # Campos somente leitura
    verbose_name_plural = 'Saldos em Criptomoedas'

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    readonly_fields = ('saldo_carteira', 'saldo_total', 'criado_em', 'atualizado_em')  # Campos somente leitura
    verbose_name_plural = 'Informações do Perfil'

class UsuarioAdminPersonalizado(UserAdmin):
    inlines = [PerfilUsuarioInline, SaldoCriptomoedasInline]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    list_display = ('username', 'email', 'exibir_saldo_wallet', 'exibir_saldos_criptomoedas', 'exibir_criado_em', 'exibir_atualizado_em')

    def exibir_saldo_wallet(self, obj):
        perfil = PerfilUsuario.objects.get(usuario=obj)
        return f"R$ {perfil.saldo_carteira:.2f}"
    exibir_saldo_wallet.short_description = 'Saldo na Wallet'

    def exibir_saldos_criptomoedas(self, obj):
        saldos = SaldoCriptomoedas.objects.filter(usuario=obj)
        if not saldos.exists():
            return "0 Criptomoedas"

        saldos_detalhados = []
        for saldo in saldos:
            saldos_detalhados.append(f"{saldo.nome}: {saldo.quantidade:.6f}")
        
        return ", ".join(saldos_detalhados)
    exibir_saldos_criptomoedas.short_description = 'Criptomoedas e Quantidades'

    def exibir_criado_em(self, obj):
        perfil = PerfilUsuario.objects.get(usuario=obj)
        return perfil.criado_em
    exibir_criado_em.short_description = 'Criado Em'

    def exibir_atualizado_em(self, obj):
        perfil = PerfilUsuario.objects.get(usuario=obj)
        return perfil.atualizado_em
    exibir_atualizado_em.short_description = 'Atualizado Em'

admin.site.unregister(User)
admin.site.register(User, UsuarioAdminPersonalizado)
