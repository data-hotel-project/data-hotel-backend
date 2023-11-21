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
        "is_working",
        "is_staff",
        "is_superuser",
        "address",
    ]
    read_only_fields = ["id", "is_superuser", "is_working"]
    extra_kwargs = {
        "password": {"write_only": True, "required": True},
        "email": {"required": True},
    }
