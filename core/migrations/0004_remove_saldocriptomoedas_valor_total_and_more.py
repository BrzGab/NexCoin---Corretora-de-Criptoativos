# Generated by Django 5.1 on 2024-08-31 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_perfilusuario_saldo_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saldocriptomoedas',
            name='valor_total',
        ),
        migrations.RemoveField(
            model_name='saldocriptomoedas',
            name='valor_unitario',
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='saldo_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
