# Generated by Django 3.0.4 on 2020-05-09 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_offer'),
        ('purchases', '0002_auto_20200509_1507'),
        ('accounts', '0004_remove_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cart',
            field=models.ManyToManyField(related_name='carrinho', to='purchases.OrderProduct'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='favorites',
            field=models.ManyToManyField(related_name='favoritos', to='produto.Product'),
        ),
    ]
