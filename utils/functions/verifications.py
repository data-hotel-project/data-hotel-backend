from copy import deepcopy
from datetime import datetime

from reservation.models import Reservation


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
    decrease_rsv_count_match = 0
    rsv_count_match = 0
    rsv_list_match = []

    rsv_list = []
    rsvs_used = []

    rsv_list_free = []
    free_unused_rooms = []
    free_unused_rooms_qt = 0

    for room in occupied_rooms:
        room_entry_date = room.entry_date.replace(tzinfo=None).date()
        room_departure_date = room.departure_date.replace(tzinfo=None).date()

        if dt_entry_date >= room_departure_date and dt_quantity <= room.quantity:
            counter += 1

        elif all_reservations:
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

            rsv_count_match = len(rsv_list_match)

            for rsv in rsv_list_match:
                if (
                    room_entry_date < rsv.entry_date.replace(tzinfo=None).date()
                    and room_departure_date
                    <= rsv.entry_date.replace(tzinfo=None).date()
                    and room.quantity >= rsv.quantity
                ):
                    rsv_list.append(rsv)
                elif rsv not in rsv_list_free:
                    rsv_list_free.append(rsv)

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
                    decrease_rsv_count_match += 1

    rsv_count_match -= decrease_rsv_count_match

    if free_rooms:
        room_quantity_matching_condition = sum(
            room.quantity >= dt_quantity for room in free_rooms
        )

        if room_quantity_matching_condition > 0 and all_reservations:
            sorted_free_rooms = sorted(free_rooms, key=lambda x: x.quantity)
            verified_rsv_ids = set()

            free_unused_rooms = deepcopy(free_rooms)

            if len(occupied_rooms) > counter:
                for room in sorted_free_rooms:
                    for rsv in rsv_list_free:
                        if (
                            rsv.quantity <= room.quantity
                            and rsv.id not in verified_rsv_ids
                            and rsv not in rsvs_used
                        ):
                            verified_rsv_ids.add(rsv.id)
                            free_unused_rooms = free_unused_rooms.exclude(id=room.id)
                            rsv_count_match -= 1
                            break

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

                rsv_count_match = len(rsv_list_match)

                for room in sorted_free_rooms:
                    for rsv in rsv_list_match:
                        if (
                            rsv.quantity <= room.quantity
                            and rsv.id not in verified_rsv_ids
                        ):
                            verified_rsv_ids.add(rsv.id)
                            free_unused_rooms = free_unused_rooms.exclude(id=room.id)
                            rsv_count_match -= 1
                            break

            free_enused_room_qt_matching_condition = sum(
                room.quantity >= dt_quantity for room in free_unused_rooms
            )

            if free_enused_room_qt_matching_condition == 0:
                free_unused_rooms_qt = 0
            else:
                free_unused_rooms_qt = len(free_unused_rooms)

    if not free_rooms:
        free_unused_rooms_qt = 0
    elif room_quantity_matching_condition == 0 or not all_reservations:
        free_unused_rooms_qt = room_quantity_matching_condition

    # print("AAAA", counter)
    # print("BBBB", rsv_count_match)
    # print("CCCC", free_unused_rooms_qt)

    return counter, rsv_count_match, free_unused_rooms_qt


def checkReservationPeriod(dt_entry, dt_departure, rsv_entry, rsv_departure):
    return (
        dt_entry >= rsv_entry.date()
        and dt_entry < rsv_departure.date()
        or (dt_entry <= rsv_entry.date() and dt_departure > rsv_entry.date())
    )
