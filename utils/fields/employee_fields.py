class EmployeeFields:
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
        "job_function",
        "admission_date",
        "is_staff",
        "is_superuser",
        "hotel",
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
