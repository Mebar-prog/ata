# Generated by Django 4.1.7 on 2023-04-21 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0006_stateuserpermission"),
    ]

    operations = [
        migrations.DeleteModel(name="StateUserPermission",),
    ]
