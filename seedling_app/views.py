from typing import override
from django.shortcuts import render

from .serializers import (
    AgroEventSerializer,
    ContractSerializer,
    UserSerializer,
    CustomerSerializer,
    DistrictSerializer,
    HouseholdSerializer,
    MahallaSerializer,
    PhotosSerializer,
    RegionSerializer,
    SeedlingSerializer,
    StatusTypesSerializer,
    SeedlingTypesSerializer,
)

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
# from django.contrib.auth import get_user_model

# User = get_user_model()


from rest_framework import viewsets, permissions

# Create your views here.

class AgroEventViewSet(viewsets.ModelViewSet):
    queryset = AgroEvent.objects.all()
    serializer_class = AgroEventSerializer
     
    


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
     


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
     


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
     


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
     


class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
     


class MahallaViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Mahalla.objects.all()
    serializer_class = MahallaSerializer
     

    @override
    def get_queryset(self):
        user = self.request.user
        return user.binded_mfy.all()
    


class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosSerializer
     
    

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
     


class SeedlingViewSet(viewsets.ModelViewSet):
    queryset = Seedling.objects.all()
    serializer_class = SeedlingSerializer
     

class StatusTypesViewSet(viewsets.ModelViewSet):
    queryset = StatusTypes.objects.all()
    serializer_class = StatusTypesSerializer


class SeedlingTypesViewSet(viewsets.ModelViewSet):
    queryset = SeedlingTypes.objects.all()
    serializer_class = SeedlingTypesSerializer
    