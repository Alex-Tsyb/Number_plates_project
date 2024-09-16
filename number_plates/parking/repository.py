from .models import Place, Session


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

            open_session_place_number = open_sessions.filter(
                place_number=palace_number
            ).first()
            if open_session_place_number is not None:
                parking_place["status"] = "busy"
                parking_place["vehicle"] = open_session_place_number.vehicle
                parking_place["start_time"] = (
                    open_session_place_number.start_time.strftime("%Y-%m-%d %H:%M")
                )
                parking_place["current_time"] = (
                    open_session_place_number.calculate_duration()
                )
                # parking_place["open_session"] = open_session_place_number

            parking_places.append(parking_place)

        place_info["parking_place"] = parking_places

        result.append(place_info)

    return result
