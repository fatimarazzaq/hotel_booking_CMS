from django.contrib import admin

from .models import User,Administrator,HallManager,Customer

# Register your models here.

admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(HallManager)
admin.site.register(Customer)
