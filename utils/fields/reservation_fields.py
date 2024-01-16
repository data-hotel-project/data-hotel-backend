class ReservationFields:
    fields = [
        "id",
        "quantity",
        "entry_date",
        "departure_date",
        "hotel",
        "guest",
        "created_at",
        "updated_at",
    ]
    read_only_fields = ["id", "created_at", "updated_at", "guest"]
