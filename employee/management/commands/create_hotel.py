from django.core.management.base import BaseCommand

from address.models import Address
from hotel.models import Hotel
from cloudinary import CloudinaryImage


url_da_imagem = "http://res.cloudinary.com/dl6chlmjd/image/upload/v1700576381/knpzctx5jnbzum0wds7t.pn"

cloudinary_image = CloudinaryImage(url_da_imagem)

address_data = {
    "street": "Avenida guanabara",
    "number": "47",
    "city": "Jacobina",
    "state": "Ba",
    "complement": "Apt",
}

address = Address.objects.create(**address_data)

hotel_data = {
    "name": "DataHotel",
    "email": "dataHotel@mail.com",
    "num_rooms": 45,
    "image": cloudinary_image,
    "address": address,
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Defina os campos")
        parser.add_argument("--email", type=str, help="Defina os campos")
        parser.add_argument("--password", type=str, help="Defina os campos")

    def handle(self, *args, **kwargs):
        hotel = Hotel.objects.create(**hotel_data)

        self.stdout.write(
            self.style.SUCCESS(f"Hotel `{hotel.name}` successfully created!")
        )
