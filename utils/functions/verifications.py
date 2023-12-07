from reservation.models import Reservation


def loopingRooms(rooms, dt_entry_date, dt_quantity=None, hotel_id_parameter=None):
    counter = 0
    all_reservations = Reservation.objects.filter(hotel=hotel_id_parameter)

    rsv_list = []
    rsvs_used = []
    for room in rooms:
        room_entry_date = room.entry_date.replace(tzinfo=None)
        room_departure_date = room.departure_date.replace(tzinfo=None)

        if dt_entry_date >= room_departure_date.date() and dt_quantity <= room.quantity:
            counter += 1

        else:
            if all_reservations:
                for rsv in all_reservations:
                    rsv_entry_date = rsv.entry_date.replace(tzinfo=None)

                    if (
                        room_entry_date.date() < rsv_entry_date.date()
                        and room_departure_date.date() <= rsv_entry_date.date()
                        and room.quantity >= rsv.quantity
                    ):
                        rsv_list.append(rsv)

                if rsv_list:
                    sorted_rsv_list = sorted(rsv_list, key=lambda x: x.entry_date)

                    if rsvs_used:
                        rsv_exist = 0
                        for sorted_rsv in sorted_rsv_list:
                            rsv_found = []
                            for rsv in rsvs_used:
                                if sorted_rsv == rsv:
                                    rsv_exist += 1
                                    rsv_found.clear()
                                    break

                                if not rsv_found:
                                    rsv_found.append(sorted_rsv)

                            if rsv_found:
                                break

                        rsv_list.clear()

                        if len(sorted_rsv_list) > rsv_exist:
                            rsvs_used.append(rsv_found[0])
                            counter += 1

                    else:
                        rsvs_used.append(sorted_rsv_list[0])
                        counter += 1
                        rsv_list.clear()

                    sorted_rsv_list.clear()

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
