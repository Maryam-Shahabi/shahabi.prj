# Generated by Django 5.1.3 on 2025-01-16 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0009_course_course_level_course_course_number_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blog",
            old_name="descreption",
            new_name="blog_descreption",
        ),
        migrations.RenameField(
            model_name="blog",
            old_name="title",
            new_name="blog_title",
        ),
        migrations.AddField(
            model_name="blog",
            name="blog_img",
            field=models.ImageField(null=True, upload_to="photo"),
        ),
    ]
