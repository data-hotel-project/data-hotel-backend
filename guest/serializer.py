from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from address.serializer import AddressSerializer
from utils.fields.guest_fields import GuestFields

from .models import Guest


class GuestSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

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


class GuestTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        from ipdb import set_trace

        # set_trace()
        username = attrs.get("username")
        password = attrs.get("password")

        # data = super().validate(attrs)
        # refresh = self.get_token(self.user)

        # data["refresh"] = str(refresh)
        # data["access"] = str(refresh.access_token)

        # return data

        if username and password:
            user = self.get_user(username)
            if user and user.check_password(password):
                refresh = self.get_token(user)

                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }

                # set_trace()
                return data

        raise serializers.ValidationError("Invalid credentials")

    def get_user(self, username):
        try:
            user = Guest.objects.get(username=username)
            return user
        except Guest.DoesNotExist:
            return None
