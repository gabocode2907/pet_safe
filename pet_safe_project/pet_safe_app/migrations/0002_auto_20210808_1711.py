# Generated by Django 3.2.6 on 2021-08-08 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pet_safe_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=50)),
                ('pet_age', models.PositiveSmallIntegerField()),
                ('pet_birth_date', models.DateField()),
                ('pet_breed', models.CharField(max_length=50)),
                ('pet_gender', models.CharField(max_length=6)),
                ('pet_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pet_color', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('pet_image', models.ImageField(upload_to='pet_image/')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('pet_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets_owner', to='pet_safe_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='PetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specie', models.CharField(max_length=50)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=50)),
                ('vaccine_date', models.DateField()),
                ('vaccine_next_date', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='vetrecord',
            name='pet_owner',
        ),
        migrations.RemoveField(
            model_name='vetrecord',
            name='rol',
        ),
        migrations.RemoveField(
            model_name='clinic',
            name='rol',
        ),
        migrations.DeleteModel(
            name='ImmunizationHistory',
        ),
        migrations.DeleteModel(
            name='vetRecord',
        ),
        migrations.AddField(
            model_name='pet',
            name='pet_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet_safe_app.pettype'),
        ),
        migrations.AddField(
            model_name='pet',
            name='vaccines',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_vaccines', to='pet_safe_app.vaccine'),
        ),
    ]