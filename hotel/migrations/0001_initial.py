# Generated by Django 4.2.7 on 2023-12-14 18:37

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('num_rooms', models.PositiveIntegerField()),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('image2', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image')),
                ('image3', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image')),
                ('image4', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image')),
                ('image5', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='address.address')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
