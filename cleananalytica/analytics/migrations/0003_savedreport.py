# Generated by Django 5.0.6 on 2024-06-20 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_client_created_at_employeerating_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
                ('data', models.JSONField()),
            ],
        ),
    ]
