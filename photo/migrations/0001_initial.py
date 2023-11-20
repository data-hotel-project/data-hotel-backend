from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hotel", "0001_initial"),
        ("room", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.ImageField(upload_to="img")),
                (
                    "hotel",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hotel_imgs",
                        to="hotel.hotel",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="room_imgs",
                        to="room.room",
                    ),
                ),
            ],
        ),
    ]
