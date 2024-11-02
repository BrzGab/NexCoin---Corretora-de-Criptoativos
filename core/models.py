from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import locale

# Define o locale para português para formatar as datas
#locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

# Classe base com herança
class BaseModel(models.Model):
    # Campo 'criado_em' registra a data e hora da criação do objeto, automaticamente preenchido
    criado_em = models.DateTimeField(auto_now_add=True)
    # Campo 'atualizado_em' registra a data e hora da última atualização do objeto, automaticamente atualizado
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        # Define que essa classe é abstrata, ou seja, não cria uma tabela no banco de dados
        abstract = True

    def __str__(self):
        # Retorna uma string representando o nome da classe e o ID do objeto
        return f"{self.__class__.__name__} (ID: {self.id})"

    # Método para formatar o campo 'criado_em' em português
    def criado_em_formatado(self):
        return self.criado_em.strftime('%d de %B de %Y, %H:%M')

    # Método para formatar o campo 'atualizado_em' em português
    def atualizado_em_formatado(self):
        return self.atualizado_em.strftime('%d de %B de %Y, %H:%M')

# Modelo para o perfil do usuário, herdando de BaseModel (demonstrando herança)
class PerfilUsuario(BaseModel):
    # Relação OneToOne com o modelo User, cada usuário tem um único PerfilUsuario
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campo para armazenar o saldo da carteira do usuário
    saldo_carteira = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Campo para armazenar o saldo total do usuário
    saldo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        # Retorna uma string representando o nome de usuário e o perfil
        return f'{self.usuario.username} - Perfil'

    # Método para calcular o saldo total de criptomoedas do usuário
    def saldo_criptomoedas(self):
        # Agrega (soma) todas as quantidades de criptomoedas associadas a esse usuário
        saldo_total_criptos = SaldoCriptomoedas.objects.filter(usuario=self.usuario).aggregate(total=models.Sum('quantidade'))['total']
        # Retorna o saldo total ou 0 se o usuário não tiver criptomoedas
        return saldo_total_criptos or 0

# Modelo para saldos de criptomoedas, herdando de BaseModel (demonstrando herança)
class SaldoCriptomoedas(BaseModel):
    # Relação ForeignKey com User, permitindo que um usuário tenha múltiplos saldos de criptomoedas (agregação)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Campo para armazenar o nome da criptomoeda (ex: Bitcoin)
    nome = models.CharField(max_length=50)
    # Campo para armazenar o símbolo da criptomoeda (ex: BTC)
    simbolo = models.CharField(max_length=10)
    # Campo para armazenar a quantidade da criptomoeda que o usuário possui
    quantidade = models.DecimalField(max_digits=20, decimal_places=8, default=0.00000000)

    def __str__(self):
        # Retorna uma string representando o nome de usuário e a criptomoeda
        return f'{self.usuario.username} - {self.nome}'

# Sinais para criar e salvar o perfil do usuário automaticamente após a criação de um User
@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Cria um PerfilUsuario associado ao User recém-criado (demonstrando composição)
        PerfilUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    # Garante que o perfil do usuário seja salvo sempre que o User for salvo
    instance.perfilusuario.save()
