# Generated by Django 3.0.4 on 2020-05-08 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrosel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carrosel',
            old_name='image',
            new_name='images',
        ),
    ]