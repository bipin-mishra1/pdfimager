# Generated by Django 4.2.5 on 2024-04-12 12:31

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ImageZipFile",
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
                ("filename", models.CharField(max_length=255)),
                ("path", models.CharField(max_length=255)),
                ("size", models.IntegerField()),
                ("uuid", models.CharField(max_length=255)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
