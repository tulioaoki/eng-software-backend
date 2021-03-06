# Generated by Django 3.0.4 on 2020-04-05 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_url', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Products Images',
                'permissions': (('geral_products images_visualizar', 'Pode visualizar Products Images'), ('geral_products images_editar', 'Pode visualizar e editar Products Images')),
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(to='produto.ProductImage'),
        ),
    ]
