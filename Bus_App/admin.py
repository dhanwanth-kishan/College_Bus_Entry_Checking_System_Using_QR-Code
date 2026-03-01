from django.contrib import admin
from Bus_App.models import *

# Register your models here.

@admin.register(StudentData)
class StudentDataAdmin(admin.ModelAdmin):
    readonly_fields = ('Qr_Code',)
    
admin.site.register(StaffData)
admin.site.register(BusData)
admin.site.register(BusEntry)

