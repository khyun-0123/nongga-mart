# Generated by Django 4.2 on 2023-08-17 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post_data_model",
            name="Time_field",
            field=models.DateTimeField(),
        ),
    ]
