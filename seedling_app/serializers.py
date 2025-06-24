from rest_framework import serializers

from .models import (
    AgroEvent,
    Contract,
    User,
    Customer,
    District,
    Household,
    Mahalla,
    Photos,
    Region,
    Seedling,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AgroEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgroEvent
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class MahallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahalla
        fields = "__all__"


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
        fields = "__all__"
