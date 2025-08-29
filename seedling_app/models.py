from enum import unique
import secrets
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.db.models import CharField, TextField
from django.contrib.auth.models import AbstractUser

# from seedling_app.admin import AgroEventAdmin

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Region(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    class Meta:
        db_table = "Region"
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class District(TimeStampedModel):
    name = CharField(max_length=255, db_index=True)
    parent_region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="tumanlar"
    )

    class Meta:
        db_table = "District"
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"
        ordering = ["name"]
        unique_together = ["name", "parent_region"]
        indexes = [
            models.Index(fields=["name", "parent_region"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.parent_region.name})"


class Mahalla(TimeStampedModel):
    name = CharField(max_length=255, db_index=True)
    parent_district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="mahallalar"
    )

    class Meta:
        db_table = "Mahalla"
        verbose_name = "Mahalla"
        verbose_name_plural = "Mahallalar"
        ordering = ["name"]
        unique_together = ["name", "parent_district"]
        indexes = [
            models.Index(fields=["name", "parent_district"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.parent_district.name})"

class CustomUser(AbstractUser):
    # Пример нового поля
    phone_number = models.CharField(max_length=20, blank=True)
    binded_mfy = models.ManyToManyField(Mahalla, blank=True)

class Household(TimeStampedModel):
    street = CharField(max_length=100)
    house = CharField(max_length=50)
    parent_mfy = models.ForeignKey(
        Mahalla, on_delete=models.CASCADE, related_name="xonadonlar"
    )
    created_by = models.ForeignKey(
        CustomUser,  # Points to Django's built-in User model
        on_delete=models.PROTECT,
        related_name="created_households",
    )
    
    class Meta:
        db_table = "Household"
        verbose_name = "Household"
        verbose_name_plural = "Households"
        ordering = ["street", "house"]
        unique_together = ["street", "house", "parent_mfy"]
        indexes = [
            models.Index(fields=["street", "house"]),
            # models.Index(fields=["qr_code"]),
        ]

    def __str__(self):
        return f"{self.street}, {self.house}"


class QrCode(TimeStampedModel):
    qr_code = CharField(max_length=255, unique=True, db_index=True)
    connected_household = models.OneToOneField(
        Household, on_delete=models.PROTECT, related_name="qr_code", null=True, blank=True
    )
    

class Customer(TimeStampedModel):
    fio = CharField(max_length=255)
    passport = CharField(max_length=50, unique=True, db_index=True)
    birthday = models.DateField()
    phone = CharField(max_length=20, unique=True, db_index=True)
    parent_household = models.ForeignKey(
        Household, on_delete=models.CASCADE, related_name="customers"
    )

    class Meta:
        db_table = "Customer"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["fio"]
        indexes = [
            models.Index(fields=["passport"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return self.fio


class Contract(TimeStampedModel):
    number = CharField(max_length=50, unique=True, db_index=True)
    date = models.DateField(auto_now_add=True)
    parent_user = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="contracts"
    )

    class Meta:
        db_table = "Contract"
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["number"]),
            models.Index(fields=["date"]),
        ]

    def __str__(self):
        return self.number


class Photos(TimeStampedModel):
    name = CharField(max_length=255)
    image = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        max_length=255,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif"])],
    )
    attached_to = models.ForeignKey(
        "AgroEvent", on_delete=models.CASCADE, related_name="photos")
    
    # content_type = models.ForeignKey(
    #     ContentType, on_delete=models.CASCADE, related_name="photos"
    # )
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        db_table = "Photos"
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
        ordering = ["-created_at"]
        indexes = [
            # models.Index(fields=["photo_type"]),
            # models.Index(fields=["object_id"]),
        ]

    def __str__(self):
        return self.name

class SeedlingTypes(TimeStampedModel):
    name = CharField(max_length=255, unique=True, db_index=True)


class Seedling(TimeStampedModel):

    seedling_type = models.ForeignKey(
        SeedlingTypes,
        on_delete=models.PROTECT,
        related_name="seedlings",
        default=1,
    )
    location = CharField(
        max_length=255, help_text="GPS coordinates or location description"
    )
    plant_status = models.ForeignKey(
        "StatusTypes",
        on_delete=models.PROTECT,
        related_name="seedlings",
    )
    plant_date = models.DateField(auto_now_add=True)
    comment = TextField(blank=True)
    parent_contract = models.ForeignKey(
        Contract, on_delete=models.PROTECT, related_name="seedlings"
    )

    class Meta:
        db_table = "Seedling"
        verbose_name = "Seedling"
        verbose_name_plural = "Seedlings"
        ordering = ["-plant_date"]
        indexes = [
            models.Index(fields=["seedling_type"]),
            models.Index(fields=["plant_status"]),
            models.Index(fields=["plant_date"]),
        ]

    def __str__(self):
        return f"{self.seedling_type} ({self.plant_status})"


class AgroEvent(TimeStampedModel):
    parent_seedling = models.ForeignKey(
        Seedling, on_delete=models.PROTECT, related_name="agro_events"
    )
    date = models.DateField(auto_now_add=True)
    comment = TextField(blank=True)
    status = models.ForeignKey(
        "StatusTypes",
        on_delete=models.PROTECT,
        related_name="agro_events",
        default=1,
    )

    class Meta:
        db_table = "AgroEvent"
        verbose_name = "Agro Event"
        verbose_name_plural = "Agro Events"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["date", "parent_seedling"]),
        ]

    def __str__(self):
        return f"{self.status} - {self.date}"


class StatusTypes(TimeStampedModel):    
    TYPES = [
        ("SEEDLING", "Seedling"),
        ("AGRO_EVENT", "Agro Event"),
    ]
    name = CharField(max_length=255, unique=True, db_index=True)
    status_for = models.CharField(max_length=20, choices=TYPES, db_index=True)

class Profile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/')
