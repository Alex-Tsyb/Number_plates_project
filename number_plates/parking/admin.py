from django.contrib import admin

# from django.contrib.auth.models import Group
from .models import Place, Session, Report


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "count_parking_place",
        "start_number",
        "exsept_numbers",
        "parking_place_numbers",
    )

    @admin.display(description="parking_place_numbers")
    def parking_place_numbers(self, obj):
        return obj.get_list_numbers_parking_place()


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "parking_place",
        "place_number",
        "vehicle",
        "start_time",
        "end_time",
        "total_cost",
        "closed",
        "used_time",
    )
    list_filter = ["start_time", "end_time"]

    @admin.display(description="closed")
    def closed(self, obj):
        return obj.end_time is not None

    @admin.display(description="used_time")
    def used_time(self, obj):
        return obj.calculate_duration()


admin.site.register(Report)

# old code
# @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
# list_display = ('license_plate', 'entry_time', 'exit_time', 'total_fee')

# def has_add_permission(self, request):
#     return request.user.is_superuser or request.user.groups.filter(name='Admin').exists()

# def has_delete_permission(self, request, obj=None):
#     return request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
