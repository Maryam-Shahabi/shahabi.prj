# Generated by Django 5.1.3 on 2025-07-01 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0002_contactmodel_alter_customuser_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseFeedback",
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
                ("name", models.CharField(max_length=100, verbose_name="نام")),
                ("email", models.EmailField(max_length=254, verbose_name="ایمیل")),
                ("message", models.TextField(verbose_name="متن دیدگاه")),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                        verbose_name="امتیاز",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main_app.product",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name": "نظرسنجی دوره",
                "verbose_name_plural": "نظرسنجی دوره\u200cها",
            },
        ),
    ]
