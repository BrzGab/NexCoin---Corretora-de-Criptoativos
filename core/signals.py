from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def sincronizar_username_com_email(sender, instance, **kwargs):
    # Antes de salvar o usuário, o username é atualizado para ser igual ao email
    instance.username = instance.email
