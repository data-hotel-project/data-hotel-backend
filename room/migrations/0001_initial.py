from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hotel", "0001_initial"),
        ("guest", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("number", models.PositiveIntegerField()),
                ("quantity", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Free", "Free"),
                            ("Occupied", "Occupied"),
                            ("Cleaning", "Cleaning"),
                            ("Under maintenance", "Maintenance"),
                        ],
                        default="Free",
                        max_length=18,
                    ),
                ),
                ("entry_date", models.DateTimeField(null=True)),
                ("departure_date", models.DateTimeField(null=True)),
                ("daily_rate", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "total_value",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0, max_digits=15
                    ),
                ),
                (
                    "guest",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="rooms",
                        to="guest.guest",
                    ),
                ),
                (
                    "hotel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to="hotel.hotel",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]
