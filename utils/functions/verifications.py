from datetime import datetime
from reservation.models import Reservation

from ipdb import set_trace


def loopingRooms(
    occupied_rooms,
    data=None,
    dt_entry_date=None,
    dt_quantity=None,
    hotel_id_parameter=None,
    free_rooms=None,
):
    if not dt_entry_date and data:
        dt_entry_date = datetime.fromisoformat(data["entry_date"]).date()

    if not dt_quantity and data:
        dt_quantity = data["quantity"]

    dt_departure_date = datetime.fromisoformat(data["departure_date"]).date()

    all_reservations = Reservation.objects.filter(hotel=hotel_id_parameter)

    counter = 0
    rsv_count_match = 0
    rsv_list_match = []

    rsv_list_free = []
    rsv_used_free = []

    rsv_list = []
    rsvs_used = []

    for room in occupied_rooms:
        room_entry_date = room.entry_date.replace(tzinfo=None).date()
        room_departure_date = room.departure_date.replace(tzinfo=None).date()

        if dt_entry_date >= room_departure_date and dt_quantity <= room.quantity:
            counter += 1

        else:
            rsv_list_match = [
                rsv
                for rsv in all_reservations
                if checkReservationPeriod(
                    dt_entry_date,
                    dt_departure_date,
                    rsv.entry_date.replace(tzinfo=None),
                    rsv.departure_date.replace(tzinfo=None),
                )
            ]

            for rsv in rsv_list_match:
                if (
                    room_entry_date < rsv.entry_date.replace(tzinfo=None).date()
                    and room_departure_date
                    <= rsv.entry_date.replace(tzinfo=None).date()
                    and room.quantity >= rsv.quantity
                ):
                    rsv_list.append(rsv)
                else:
                    if rsv not in rsv_list_free:
                        rsv_list_free.append(rsv)

            # rsv_list = [
            #     rsv
            #     for rsv in rsv_list_match
            #     if (
            #         room_entry_date < rsv.entry_date.replace(tzinfo=None).date()
            #         and room_departure_date
            #         <= rsv.entry_date.replace(tzinfo=None).date()
            #         and room.quantity >= rsv.quantity
            #     )
            # ]

            rsv_count_match = len(rsv_list_match)

            if rsv_list:
                latest_unused_rsv = next(
                    (
                        rsv
                        for rsv in sorted(rsv_list, key=lambda x: x.entry_date)
                        if rsv not in rsvs_used
                    ),
                    None,
                )

                rsv_list.clear()

                if latest_unused_rsv:
                    rsvs_used.append(latest_unused_rsv)
                    counter += 1

    if free_rooms:
        for room in free_rooms:
            set_trace()

    return counter, rsv_count_match


def checkReservationPeriod(dt_entry, dt_departure, rsv_entry, rsv_departure):
    return (
        dt_entry >= rsv_entry.date()
        and dt_entry < rsv_departure.date()
        or (dt_entry <= rsv_entry.date() and dt_departure > rsv_entry.date())
    )
