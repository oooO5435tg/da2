from django.contrib import admin
from .models import Service, User, Order, Profile


admin.site.register(User)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Profile)
