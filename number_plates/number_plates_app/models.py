from django.db import models


# class ParkingPlase(models.Model):
#     description = models.CharField(max_length=255)
#     count_parking_plase = models.IntegerField()


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
        "total_cars": total_cars,
        "blocked_cars": blocked_cars,
        "total_parking_sessions": total_parking_sessions,
        "total_profit": total_profit,
    }
