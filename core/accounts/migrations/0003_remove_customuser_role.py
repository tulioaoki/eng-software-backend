# Generated by Django 3.0.4 on 2020-04-03 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200403_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
    ]
