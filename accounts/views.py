from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from .forms import (
    DoctorForm,
    PatientForm,
    CreateUserForm,
    AppointmentForm,
    PrescriptionForm,
    InvoiceForm,
)
from .decorators import unauthenticated_user, allowed_users, hr_only, recep_only
from .models import Doctor, Patient, Appointment, Prescription, Accounting


@unauthenticated_user
def home(request):
    return render(request, "accounts/home.html")


@unauthenticated_user
def registerDoc(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="doctor")
            user.groups.add(group)
            return redirect("login")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def registerPat(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="patient")
            user.groups.add(group)
            return redirect("login")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.groups.filter(name="hr").exists():
            login(request, user)
            return redirect("hrhome")
        elif user is not None and user.groups.filter(name="receptionist").exists():
            login(request, user)
            return redirect("recephome")
        elif user is not None and user.groups.filter(name="doctor").exists():
            login(request, user)
            return redirect("doctor")
        elif user is not None and user.groups.filter(name="patient").exists():
            login(request, user)
            return redirect("patient")

        else:
            messages.info(request, "Username OR password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
@hr_only
def hrhome(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    total_doctors = doctors.count()
    active = doctors.filter(status="Active").count()

    total_patients = patients.count()

    context = {
        "doctors": doctors,
        "patients": patients,
        "total_doctors": total_doctors,
        "active": active,
        "total_patients": total_patients,
    }
    return render(request, "accounts/hrdashboard.html", context)


@login_required(login_url="login")
@recep_only
def recephome(request):
    appointments = Appointment.objects.all()
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()

    total_appointments = appointments.count()
    completed = appointments.filter(status="Completed").count()
    pending = appointments.filter(status="Pending").count()

    context = {
        "appointments": appointments,
        "doctors": doctors,
        "patients": patients,
        "total_appointments": total_appointments,
        "completed": completed,
        "pending": pending,
    }
    return render(request, "accounts/recepdash.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["doctor"])
def doctor(request):
    patients = request.user.doctor.patient_set.all()
    appointments = request.user.doctor.appointment_set.all()
    prescriptions = request.user.doctor.prescription_set.all()

    context = {
        "patients": patients,
        "appointments": appointments,
        "prescriptions": prescriptions,
    }
    return render(request, "accounts/doctor.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["patient"])
def patient(request):
    appointments = request.user.patient.appointment_set.all()
    prescriptions = request.user.patient.prescription_set.all()

    context = {
        "appointments": appointments,
        "prescriptions": prescriptions,
    }
    return render(request, "accounts/patient.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["hr"])
def addDoctor(request):
    form = DoctorForm()
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("hrhome")
    context = {
        "form": form,
    }
    return render(request, "accounts/docUpdate.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["doctor", "hr"])
def updateDoctor(request, pk):
    doctor = Doctor.objects.get(user_id=pk)
    form = DoctorForm(instance=doctor)
    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            if request.user.groups.filter(name="hr").exists():
                return redirect("hrhome")
            if request.user.groups.filter(name="doctor").exists():
                return redirect("doctor")

    context = {
        "form": form,
        "doctor": doctor,
    }
    return render(request, "accounts/docUpdate.html", context)


@login_required(login_url="login")
@hr_only
def deleteDoctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    if request.method == "POST":
        doctor.delete()
        return redirect("hrhome")

    context = {"doctor": doctor}
    return render(request, "accounts/delDoc.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["receptionist"])
def addPatient(request):
    form = PatientForm()
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recephome")
    context = {"form": form}
    return render(request, "accounts/patUpdate.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["patient", "receptionist"])
def updatePatient(request, pk):
    patient = Patient.objects.get(user_id=pk)
    form = PatientForm(instance=patient)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            if request.user.groups.filter(name="receptionist").exists():
                return redirect("recephome")
            elif request.user.groups.filter(name="patient").exists():
                return redirect("patient")

    context = {"form": form}
    return render(request, "accounts/patUpdate.html", context)


@login_required(login_url="/")
@recep_only
def deletePatient(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        patient.delete()
        return redirect("recephome")
    context = {"patient": patient}
    return render(request, "accounts/delPat.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["doctor", "patient", "receptionist"])
def appointments(request):
    user = request.user
    if user.groups.filter(name="doctor"):
        appointments = request.user.doctor.appointment_set.all()
    elif user.groups.filter(name="patient"):
        appointments = request.user.patient.appointment_set.all()
    elif user.groups.filter(name="receptionist"):
        appointments = Appointment.objects.all()
    context = {
        "appointments": appointments,
    }
    return render(request, "accounts/appointments.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["receptionist", "doctor"])
def createAppoint(request):
    form = AppointmentForm()
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("appointments")
    context = {"form": form}
    return render(request, "accounts/createappoint.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["doctor", "receptionist"])
def updateAppoint(request, pk):
    appointment = Appointment.objects.get(id=pk)
    form = AppointmentForm(instance=appointment)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("appointments")
    context = {
        "form": form,
    }
    return render(request, "accounts/appointUpdate.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["receptionist", "doctor"])
def deleteAppoint(request, pk):
    appointment = Appointment.objects.get(id=pk)
    if request.method == "POST":
        appointment.delete()
        return redirect("appointments")
    context = {
        "appointment": appointment,
    }
    return render(request, "accounts/delAppoint.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["doctor", "patient"])
def prescriptions(request):
    user = request.user
    if user.groups.filter(name="doctor").exists():
        prescriptions = request.user.doctor.prescription_set.all()
    if user.groups.filter(name="patient").exists():
        prescriptions = request.user.patient.prescription_set.all()

    context = {
        "prescriptions": prescriptions,
    }
    return render(request, "accounts/prescriptions.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["doctor"])
def createPres(request):
    form = PrescriptionForm()
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("prescriptions")
    context = {"form": form}
    return render(request, "accounts/createpres.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["doctor"])
def updatePres(request, pk):
    prescription = Prescription.objects.get(id=pk)
    form = PrescriptionForm(instance=prescription)
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect("prescriptions")
    context = {
        "form": form,
        "prescription": prescription,
    }
    return render(request, "accounts/presUpdate.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["doctor"])
def deletePres(request, pk):
    prescription = Prescription.objects.get(id=pk)
    if request.method == "POST":
        prescription.delete()
        return redirect("prescriptions")
    context = {
        "prescription": prescription,
    }
    return render(request, "accounts/delPres.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["receptionist", "hr", "patient"])
def invoice(request):
    if request.user.groups.filter(name="patient").exists():
        accounts = request.user.patient.accounting_set.all()
    else:
        accounts = Accounting.objects.all()

    context = {
        "accounts": accounts,
    }
    return render(request, "accounts/invoice.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["hr", "receptionist"])
def generateInvoice(request):
    form = InvoiceForm()
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("invoice")
    context = {
        "form": form,
    }
    return render(request, "accounts/createInv.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["hr", "receptionist"])
def updateInv(request, pk):
    account = Accounting.objects.get(id=pk)
    form = InvoiceForm(instance=account)
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect("invoice")
    print(form.errors)
    context = {
        "form": form,
    }
    return render(request, "accounts/invUpdate.html", context)
