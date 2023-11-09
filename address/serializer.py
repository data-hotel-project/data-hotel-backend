from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        # fields = ["id", "street", "number", "city", "state", "complement"]
