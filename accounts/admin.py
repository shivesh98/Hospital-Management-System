from django.contrib import admin

from .models import HR, Receptionist, Doctor, Patient, Appointment, Prescription

admin.site.register(HR)
admin.site.register(Receptionist)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)
