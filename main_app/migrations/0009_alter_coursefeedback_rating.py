# Generated by Django 5.1.3 on 2025-07-04 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0008_alter_coursefeedback_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursefeedback",
            name="rating",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                null=True,
                verbose_name="امتیاز",
            ),
        ),
    ]
