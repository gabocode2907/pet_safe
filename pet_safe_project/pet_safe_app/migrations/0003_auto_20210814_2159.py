# Generated by Django 3.2.6 on 2021-08-15 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_safe_app', '0002_alter_pet_pet_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='is_lost',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pet',
            name='pet_age',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]