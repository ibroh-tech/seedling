from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()


from .models import (
    AgroEvent,
    Contract,
    Customer,
    District,
    Household,
    Mahalla,
    Photos,
    Region,
    Seedling,
    StatusTypes,
    SeedlingTypes,
    CustomUser
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class AgroEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgroEvent
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'number', 'date']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'fio', 'passport', 'birthday', 'phone']


class MahallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahalla
        fields = ['id', 'name', 'parent_district']


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = "__all__"


class SeedlingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seedling
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ['id', 'street', 'house', 'parent_mfy', "created_at"]

class StatusTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTypes
        fields = ['id', 'name', 'status_for']

class SeedlingTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedlingTypes
        fields = ['id', 'name']