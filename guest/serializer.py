from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from address.serializer import AddressSerializer
from utils.auth.authentication import EmailOrUsernameModelBackend
from utils.fields.guest_fields import GuestFields

from .models import Guest


class GuestSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Guest.objects.all())],
    )

    def create(self, validated_data: dict) -> Guest:
        address_data = validated_data.pop("address")

        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)

        address_data = address_serializer.save()

        validated_data["address"] = address_data

        return Guest.objects.create_user(**validated_data)

    def update(self, instance: Guest, validated_data: dict) -> Guest:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Guest
        fields = GuestFields.fields
        extra_kwargs = GuestFields.extra_kwargs


class GuestTokenSerializer(TokenObtainPairSerializer, EmailOrUsernameModelBackend):
    # from ipdb import set_trace
    # set_trace()
    print("AAAAAAAAA")
    pass
