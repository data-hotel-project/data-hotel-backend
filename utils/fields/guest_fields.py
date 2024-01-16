class GuestFields:
    fields = [
        "id",
        "username",
        "email",
        "password",
        "birthdate",
        "nationality",
        "contact",
        "aditional_contact",
        "emergency_num",
        "is_staff",
        "is_superuser",
        "address",
        "created_at",
        "updated_at",
    ]
    read_only_fields = [
        "id",
        "is_superuser",
        "created_at",
        "updated_at",
    ]
    extra_kwargs = {
        "password": {"write_only": True, "required": True},
        "email": {"required": True},
    }
