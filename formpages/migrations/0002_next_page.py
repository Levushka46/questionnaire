# Generated by Django 5.0.4 on 2024-04-27 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("formpages", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="next_page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="previous_pages",
                to="formpages.page",
                verbose_name="next page",
            ),
        ),
    ]
