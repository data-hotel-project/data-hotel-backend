# Generated by Django 4.2.7 on 2023-11-09 12:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_rename_complemente_address_complement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
