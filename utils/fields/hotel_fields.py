class HotelFields:
    fields = [
        "id",
        "name",
        "email",
        "num_rooms",
        "image",
        "image2",
        "image3",
        "image4",
        "image5",
        "full_url",
        "full_url2",
        "full_url3",
        "full_url4",
        "full_url5",
        "address",
        "created_at",
        "updated_at",
    ]
    read_only_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
    extra_kwargs = {
        "image": {"write_only": True},
        "image2": {"write_only": True},
        "image3": {"write_only": True},
        "image4": {"write_only": True},
        "image5": {"write_only": True},
    }
