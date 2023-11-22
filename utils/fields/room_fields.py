class RoomFields:
    fields = [
        "id",
        "number",
        "status",
        "quantity",
        "entry_date",
        "departure_date",
        "daily_rate",
        "total_value",
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
        "hotel",
    ]
    read_only_fields = ["id"]
    extra_kwargs = {
        "image": {"write_only": True},
        "image2": {"write_only": True},
        "image3": {"write_only": True},
        "image4": {"write_only": True},
        "image5": {"write_only": True},
    }
