# Generated by Django 3.2.6 on 2021-08-13 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_safe_app', '0008_alter_pet_pet_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='pet_age',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]