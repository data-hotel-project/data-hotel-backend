# seuapp/management/commands/createsuperuser_without_relations.py

# from django.contrib.auth import get_user_model
# from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string




from django.core.management.base import BaseCommand, CommandError
from employee.models import Employee
from address.models import Address
from hotel.models import Hotel

address_data = {
			"street": f"{get_random_string(12)}",
			"number": "...",
			"city": "...",
			"state": "...",
			"complement": "..."
	    }

address = Address.objects.create(**address_data)

hotel_data = {
	"name": "...",
	"email": f"{get_random_string(12)}@mail.com",
	"password": "...",
	"num_rooms": 00,
	"address": address
}

print("address:", address_data["street"])
print("hotel:", hotel_data["email"])

hotel = Hotel.objects.create(**hotel_data)

class Command(BaseCommand):

    help = 'Cria um superusuário ignorando os relacionamentos do Employee model'

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
        # hotel = Hotel.objects.create(**hotel_data)
        
        print(hotel)
        print(address)

        userFound = Employee.objects.filter(username=username).exists()
        emailFound = Employee.objects.filter(email=email).exists()

        if userFound:
            raise CommandError(f"Username `{username}` already taken.")
        if emailFound:
            raise CommandError(f"Email `{email}` already taken.")
        Employee.objects.create_superuser(username=username, email=email, password=password, address=address, hotel=hotel, birthdate="2000-01-01", nationality="any", contact="xxxxx", emergency_num="yyyyyyyy")
        self.stdout.write(
            self.style.SUCCESS(f"Admin `{username}` successfully created!")
        )
        
        












# class Command(BaseCommand):
#     help = 'Cria um superusuário ignorando os relacionamentos do Employee model'

#     def handle(self, *args, **options):
#         User = get_user_model()
        
#         username = input('Digite o nome de usuário para o superusuário: ')
#         password = get_random_string()  # Gera uma senha aleatória

#         # Crie o superusuário
#         superuser = User.objects.create_superuser(
#             username=username,
#             password=password,
#             birthdate='1990-01-01',  # Substitua com a data de nascimento desejada
#             nationality='sua_nacionalidade',
#             contact='seu_contato',
#             emergency_num='num_emergencia',
#             job_function='Admin',
#             is_working=True,
#         )

#         print(f'Superusuário criado com sucesso: {superuser.username}')
