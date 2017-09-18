from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Products)
admin.site.register(Productcategories)
admin.site.register(Reviews)
admin.site.register(Users)
admin.site.register(Orders)
admin.site.register(Orderdetails)