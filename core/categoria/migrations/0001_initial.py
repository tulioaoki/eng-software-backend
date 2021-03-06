# Generated by Django 3.0.4 on 2020-04-03 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'permissions': (('geral_categories_visualizar', 'Pode visualizar Categories'), ('geral_categories_editar', 'Pode visualizar e editar Categories')),
                'default_permissions': (),
            },
        ),
    ]
