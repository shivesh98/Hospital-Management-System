from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment, Prescription, Accounting


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"


class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = "__all__"


class InvoiceForm(ModelForm):
    class Meta:
        model = Accounting
        fields = "__all__"
