from django.contrib import admin
from insure_your_buddy.models import *
from users.models import User

# Register your models here.
admin.site.register(InsuranceService)
admin.site.register(Customer)
admin.site.register(User)
