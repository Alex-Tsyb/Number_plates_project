from .models import Place, Session

from cars.models import Car


def generate_admin_statistics():
    # total_cars = Car.objects.count()
    # blacklisted_cars = Car.objects.filter(blacklisted=True).count()
    # total_parking_sessions = Car.objects.exclude(exit_time=None).count()
    # total_profit = sum(car.total_fee for car in Car.objects.exclude(total_fee=0))

    total_cars = 100
    blocked_cars = 1
    total_parking_sessions = 10
    total_profit = 50
    return {
        "total_vehicles": total_cars,
        "blocked_vehicles": blocked_cars,
        "total_parking_sessions": total_parking_sessions,
        "total_profit": total_profit,
    }


def get_session_by_id(session_id: int):
    return Session.objects.get(pk=session_id)

def get_session_by_id_for_form(session_id: int):

    session_by_id = get_session_by_id(session_id)

    session_obj = {}

    session_obj["parking_place"] = session_by_id.parking_place
    session_obj["place_number"] = session_by_id.place_number
    session_obj["vehicle"] = session_by_id.vehicle
    session_obj["start_time"] = session_by_id.start_time
    session_obj["end_time"] = session_by_id.end_time
    session_obj["total_cost"] = session_by_id.total_cost
    session_obj["closed"] = session_by_id.end_time is not None

    return session_obj

def get_not_closed_sessions(place: Place = None):
    if not place is None:
        return Session.objects.filter(end_time__isnull=True, parking_place=place)
    else:
        return Session.objects.filter(end_time__isnull=True)


def get_places_info():
    result = []
    for place in Place.objects.all():
        place_info = {}
        place_info["description"] = place

        numbers_parking_place = place.get_list_numbers_parking_place()

        # place_result["numbers_parking_place"] = numbers_parking_place

        parking_places = []

        open_sessions = get_not_closed_sessions(place=place)

        for palace_number in numbers_parking_place:
            parking_place = {}
            parking_place["number"] = palace_number
            parking_place.setdefault("status", "free")
            parking_place.setdefault("vehicle", None)
            parking_place.setdefault("start_time", None)
            parking_place.setdefault("session_id", None)

            open_session_place_number = open_sessions.filter(
                place_number=palace_number
            ).first()
            if not open_session_place_number is None:
                parking_place["status"] = "busy"
                parking_place["vehicle"] = open_session_place_number.vehicle
                parking_place["start_time"] = (
                    open_session_place_number.start_time.strftime("%Y-%m-%d %H:%M")
                )
                parking_place["current_time"] = (
                    open_session_place_number.calculate_duration()
                )
                parking_place["session_id"] = str(open_session_place_number.id)

            parking_places.append(parking_place)

        place_info["parking_place"] = parking_places

        result.append(place_info)

    return result


def get_free_parking_places_for_choice(place: Place = None):
    if place is None:
        return (1,2,3,4)
    return place.get_list_numbers_parking_place()


def get_cars_for_choice():

    return Car.objects.all()