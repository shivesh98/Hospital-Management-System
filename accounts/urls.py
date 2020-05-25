from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register-doctor/", views.registerDoc, name="register-doctor"),
    path("register-patient/", views.registerPat, name="register-patient"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("hr/", views.hrhome, name="hrhome"),
    path("receptionist/", views.recephome, name="recephome"),
    path("doctor/", views.doctor, name="doctor"),
    path("patient/", views.patient, name="patient"),
    path("add-doctor/", views.addDoctor, name="add-doctor"),
    path("update-doctor/<pk>/", views.updateDoctor, name="update-doctor"),
    path("delete-doctor/<pk>/", views.deleteDoctor, name="delete-doctor"),
    path("add-patient/", views.addPatient, name="add-patient"),
    path("update-patient/<pk>/", views.updatePatient, name="update-patient"),
    path("delete-patient/<pk>/", views.deletePatient, name="delete-patient"),
    path("appointments/", views.appointments, name="appointments"),
    path("create-appointment/", views.createAppoint, name="create-appoint"),
    path("update-appointment/<pk>/", views.updateAppoint, name="update-appoint"),
    path("delete-appointment/<pk>/", views.deleteAppoint, name="delete-appoint"),
    path("prescriptions/", views.prescriptions, name="prescriptions"),
    path("create-prescription/", views.createPres, name="create-pres"),
    path("update-prescription/<pk>/", views.updatePres, name="update-pres"),
    path("delete-prescription/<pk>/", views.deletePres, name="delete-pres"),
    path("invoices/", views.invoice, name="invoice"),
    path("generate-invoice/", views.generateInvoice, name="create-invoice"),
    path("update-invoice/<pk>/", views.updateInv, name="update-invoice"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
]
