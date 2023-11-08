# Generated by Django 4.2.7 on 2023-11-08 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('num_rooms', models.PositiveIntegerField()),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='address.address')),
            ],
        ),
    ]
