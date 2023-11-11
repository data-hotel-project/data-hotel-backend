class GuestFields:
    fields = [
        "id",
        "username",
        "email",
        "password",
        "birthdate",
        "nationality",
        "contact",
        "contact_aditional",
        "emergency_num",
        "address",
        "is_staff",
        "is_superuser",
    ]
    read_only_fields = ["id", "is_superuser"]
    extra_kwargs = {
        "password": {"write_only": True, "required": True},
        "email": {"required": True},
    }
