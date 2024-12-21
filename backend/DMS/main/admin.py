from django.contrib import admin
from .models import Component
from .models import Vehicle
from .models import Issue
from .models import Bill, Service

# Register your models here.
admin.site.register(Component)
admin.site.register(Vehicle)
admin.site.register(Issue)
admin.site.register(Bill)
admin.site.register(Service)