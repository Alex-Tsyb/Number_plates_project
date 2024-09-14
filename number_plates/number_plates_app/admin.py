from django.contrib import admin
from django.contrib.auth.models import Group
from cars.models import Car

# @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
    # list_display = ('license_plate', 'entry_time', 'exit_time', 'total_fee')

    # def has_add_permission(self, request):
    #     return request.user.is_superuser or request.user.groups.filter(name='Admin').exists()

    # def has_delete_permission(self, request, obj=None):
    #     return request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
