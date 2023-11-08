from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Guest
# from address.serializer import AddressSerializer


class GuestSerializer(serializers.ModelSerializer):
    # address = AddressSerializer()

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Guest.objects.all())],
    )

    class Meta:
        model = Guest
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
        }
        depth = 1
