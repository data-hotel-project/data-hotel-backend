# Generated by Django 4.2.7 on 2023-11-10 19:41

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
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('num_rooms', models.PositiveIntegerField()),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='address.address')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
