# Generated by Django 4.2.7 on 2023-11-13 20:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('street', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=3)),
                ('complement', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
