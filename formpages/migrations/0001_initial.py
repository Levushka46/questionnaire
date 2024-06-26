# Generated by Django 5.0.4 on 2024-04-26 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Page",
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
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
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
                (
                    "text",
                    models.CharField(max_length=255, verbose_name="question text"),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("line", "single line text"), ("select", "select")],
                        default="line",
                        max_length=32,
                        verbose_name="question type",
                    ),
                ),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="order on the page"
                    ),
                ),
                (
                    "required",
                    models.BooleanField(default=False, verbose_name="required"),
                ),
                (
                    "multiple_choice",
                    models.BooleanField(default=False, verbose_name="multiple choice"),
                ),
                (
                    "page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="questions",
                        to="formpages.page",
                        verbose_name="page",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SelectOption",
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
                ("text", models.CharField(max_length=255, verbose_name="option text")),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="option order"
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="options",
                        to="formpages.question",
                        verbose_name="question",
                    ),
                ),
            ],
        ),
    ]
