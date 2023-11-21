from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string

from address.models import Address
from employee.models import Employee
from hotel.models import Hotel
from datetime import datetime
import pytz

address_data = {
    "street": f"{get_random_string(12)}",
    "number": "...",
    "city": "...",
    "state": "...",
    "complement": "...",
}

address = Address.objects.create(**address_data)

hotel_data = {
    "name": f"{get_random_string(12)}admin",
    "email": f"{get_random_string(12)}@mail.com",
    "num_rooms": 00,
    "address": address,
}

hotel = Hotel.objects.create(**hotel_data)

birthdate = datetime.strptime("2001-01-15", "%Y-%m-%d").replace(tzinfo=pytz.UTC)

employee_data_partial = {
    "birthdate": birthdate,
    "nationality": "...",
    "contact": "xxxxx",
    "emergency_num": "yyyyyyyy",
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Defina os campos")
        parser.add_argument("--email", type=str, help="Defina os campos")
        parser.add_argument("--password", type=str, help="Defina os campos")

    def handle(self, *args, **kwargs):
        username = kwargs.get("username")
        username = username if username else "admin"
        email = kwargs.get("email")
        email = email if email else f"{username}@example.com"
        password = kwargs.get("password")
        password = password if password else "admin1234"

        userFound = Employee.objects.filter(username=username).exists()
        emailFound = Employee.objects.filter(email=email).exists()

        if userFound:
            raise CommandError(f"Username `{username}` already taken.")
        if emailFound:
            raise CommandError(f"Email `{email}` already taken.")

        Employee.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            address=address,
            hotel=hotel,
            **employee_data_partial,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Admin `{username}` successfully created!")
        )
