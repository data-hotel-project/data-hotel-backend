# Generated by Django 4.2.7 on 2023-11-20 15:33

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        ('hotel', '0001_initial'),
        ('customUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('job_function', models.CharField(choices=[('Admin', 'Admin'), ('Receptionist', 'Receptionist'), ('Regular', 'Regular')], default='Regular', max_length=20)),
                ('admission_date', models.DateTimeField(auto_now_add=True)),
                ('is_working', models.BooleanField(default=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='address.address')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='hotel.hotel')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=('customUser.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
