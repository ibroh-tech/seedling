from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Mahalla, District, Region, Household, Customer, Contract, Photos, Seedling, AgroEvent, StatusTypes, SeedlingTypes

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
        # поля при редактировании существующего пользователя
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {
            "fields": ("phone_number", "binded_mfy"),
        }),
    )

    # поля при создании нового пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительная информация", {
            "classes": ("wide",),
            "fields": ("phone_number", "binded_mfy"),
        }),
    )

    # для отображения в списке
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "phone_number")

@admin.register(Mahalla)
class MahallaAdmin(admin.ModelAdmin):
    model = Mahalla

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    model = District
    

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    model = Region
    

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    model = Household


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = Customer


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    model = Contract


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    model = Photos


@admin.register(Seedling)
class SeedlingAdmin(admin.ModelAdmin):
    model = Seedling


@admin.register(AgroEvent)
class AgroEventAdmin(admin.ModelAdmin):
    model = AgroEvent

@admin.register(StatusTypes)
class StatusTypesAdmin(admin.ModelAdmin):
    model = StatusTypes

@admin.register(SeedlingTypes)
class SeedlingTypesAdmin(admin.ModelAdmin):
    model = SeedlingTypes
