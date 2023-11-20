class HotelFields:
    fields = [
        "id",
        "name",
        "email",
        "num_rooms",
        "address",
        "image",
        "full_url",
    ]
    read_only_fields = ["id"]
    extra_kwargs = {}
