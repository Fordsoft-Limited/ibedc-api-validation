from django.contrib import admin
from .models import (Customer, CustomerBatch)

# admin.site.register(CustomerBatch, Customer)
admin.site.register(CustomerBatch)
admin.site.register(Customer)