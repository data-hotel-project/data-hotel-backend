# Generated by Django 4.2.7 on 2023-11-08 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=3)),
                ('complemente', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
