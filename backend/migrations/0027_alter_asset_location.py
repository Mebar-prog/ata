# Generated by Django 4.1.7 on 2023-06-03 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0026_reportlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
