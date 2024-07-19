from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(buyer)
admin.site.register(seller)
admin.site.register(item)
admin.site.register(invoice)
admin.site.register(employee)
admin.site.register(users_copy)