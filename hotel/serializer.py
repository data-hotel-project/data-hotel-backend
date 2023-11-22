from rest_framework import serializers

from address.models import Address
from address.serializer import AddressSerializer
from utils.fields.hotel_fields import HotelFields

from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    full_url = serializers.SerializerMethodField()
    full_url2 = serializers.SerializerMethodField()
    full_url3 = serializers.SerializerMethodField()
    full_url4 = serializers.SerializerMethodField()
    full_url5 = serializers.SerializerMethodField()

    def get_full_url(self, obj):
        if obj.image:
            return obj.image.url

    def get_full_url2(self, obj):
        if obj.image2:
            return obj.image2.url

    def get_full_url3(self, obj):
        if obj.image3:
            return obj.image3.url

    def get_full_url4(self, obj):
        if obj.image4:
            return obj.image4.url

    def get_full_url5(self, obj):
        if obj.image5:
            return obj.image5.url

    def create(self, validated_data: dict) -> Hotel:
        address_data = validated_data.pop("address")

        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)

        address, created = Address.objects.get_or_create(**address_data)

        if not created:
            raise serializers.ValidationError(
                {"address": ["hotel with this address already exists."]}
            )

        validated_data["address"] = address

        return Hotel.objects.create(**validated_data)

    def update(self, instance: Hotel, validated_data: dict) -> Hotel:
        address_instance = instance.address

        address_data = validated_data.get("address", {})

        is_address_changed = any(
            getattr(address_instance, field) != value
            for field, value in address_data.items()
        )

        if is_address_changed:
            combined_data = {**address_instance.__dict__, **address_data}

            combined_data.pop("_state", None)
            combined_data.pop("id", None)

            existing_address = Address.objects.filter(**combined_data).first()

        if existing_address:
            hotel = Hotel.objects.filter(address=existing_address).exists()

            if hotel:
                raise serializers.ValidationError(
                    {"address": ["hotel with this address already exists."]}
                )

            instance.address = existing_address
        else:
            new_address_instance = Address.objects.create(
                street=address_data.get("street", address_instance.street),
                number=address_data.get("number", address_instance.number),
                city=address_data.get("city", address_instance.city),
                state=address_data.get("state", address_instance.state),
                complement=address_data.get("complement", address_instance.complement),
            )

            instance.address = new_address_instance
            instance.save()

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            elif key == "address":
                pass
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Hotel
        fields = HotelFields.fields
        extra_kwargs = HotelFields.extra_kwargs
