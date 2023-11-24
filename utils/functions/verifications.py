def loopingRooms(rooms, dt_entry_date):
    counter = 0
    for room in rooms:
        room_departure_date = room.departure_date.replace(tzinfo=None)

        if dt_entry_date >= room_departure_date.date():
            counter += 1

    return counter


def checkReservationPeriod(dt_entry, dt_departure, rsv_entry, rsv_departure):
    boolean = False
    if (
        dt_entry >= rsv_entry.date()
        and dt_entry < rsv_departure.date()
        or (dt_entry <= rsv_entry.date() and dt_departure > rsv_entry.date())
    ):
        boolean = True

    return boolean
