from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from PIL import Image
import random
import string

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)
STATUS = (
    ("Active", "Active"),
    ("Inactive", "Inactive"),
)
CHECK = (
    ("Pending", "Pending"),
    ("Completed", "Completed"),
)


class HR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    gender = models.CharField(max_length=100, choices=GENDER)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return self.user.username

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    gender = models.CharField(max_length=100, choices=GENDER)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return self.user.username

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True)
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=100, choices=GENDER)
    age = models.CharField(max_length=3)
    address = models.CharField(max_length=255)
    department = models.CharField(max_length=100, null=False, blank=False)
    salary = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=200, null=False, blank=False, choices=STATUS)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    disease = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True)
    contact = models.IntegerField()
    gender = models.CharField(max_length=100, choices=GENDER)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=3)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True)
    status = models.CharField(max_length=50, choices=CHECK)

    def __str__(self):
        return str(self.date)


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescription = models.CharField(max_length=300)
    disease = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.prescription


class Accounting(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    medicines = models.CharField(max_length=200, null=True)
    medicines_price = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    consultation_price = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    paid = models.CharField(max_length=255)
    outstanding = models.CharField(max_length=255)
    total = models.CharField(max_length=255)

    def __str__(self):
        return self.patient.name
