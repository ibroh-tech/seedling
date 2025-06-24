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
)

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

from rest_framework import viewsets, permissions

# Create your views here.

class AgroEventViewSet(viewsets.ModelViewSet):
    queryset = AgroEvent.objects.all()
    serializer_class = AgroEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [permissions.IsAuthenticated]


class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    permission_classes = [permissions.IsAuthenticated]


class MahallaViewSet(viewsets.ModelViewSet):
    queryset = Mahalla.objects.all()
    serializer_class = MahallaSerializer
    permission_classes = [permissions.IsAuthenticated]
    


class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SeedlingViewSet(viewsets.ModelViewSet):
    queryset = Seedling.objects.all()
    serializer_class = SeedlingSerializer
    permission_classes = [permissions.IsAuthenticated]