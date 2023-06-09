# Generated by Django 4.1.7 on 2023-04-21 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0007_delete_stateuserpermission"),
    ]

    operations = [
        migrations.CreateModel(
            name="StateUserPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("can_view_report_and_profile", "Can view report and profile")
                ],
            },
        ),
    ]
