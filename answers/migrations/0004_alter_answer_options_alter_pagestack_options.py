# Generated by Django 5.0.4 on 2024-04-29 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("answers", "0003_answers_related_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={"verbose_name": "answer", "verbose_name_plural": "answers"},
        ),
        migrations.AlterModelOptions(
            name="pagestack",
            options={
                "verbose_name": "page stack",
                "verbose_name_plural": "page stacks",
            },
        ),
    ]
