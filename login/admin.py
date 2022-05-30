from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from booking.models import Contact, Rental, Booking

User = get_user_model()

admin.site.register(User, UserAdmin)
admin.site.register(Contact)
admin.site.register(Rental)
admin.site.register(Booking)
