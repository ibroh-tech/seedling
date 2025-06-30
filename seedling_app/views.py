from typing import override
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

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


from rest_framework import views, viewsets, permissions

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
    
class CustomAddRecordView(views.APIView):
    def post(self, request):
        # Access custom data from request body
        mahalla_id = request.data.get('mahalla_id')
        user_mfy = request.user.binded_mfy.all()
        if Mahalla.objects.get(id=mahalla_id) not in user_mfy:
            return Response({"error": "You are not allowed to add record to this mahalla"}, status=status.HTTP_400_BAD_REQUEST)
        
        household_street = request.data.get('street')
        household_number = request.data.get('house_number')
        try:
            household, created = Household.objects.get_or_create(
                street=household_street,
                house=household_number,
                parent_mfy=Mahalla.objects.get(id=mahalla_id),
                created_by=request.user,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        customer_fio = request.data.get('fio')
        customer_pass = request.data.get('passport')
        customer_birthday = request.data.get('birthday')
        customer_phone = request.data.get('phone')
        try:
            customer, created = Customer.objects.get_or_create(
                fio=customer_fio,
                passport=customer_pass,
                birthday=customer_birthday,
                phone=customer_phone,
            parent_household=household
            ) 
        except Exception as e:
            household.delete()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


        contract_number = request.data.get('contract_number')
        contract_date = request.data.get('contract_date')
        try:
            contract, created = Contract.objects.get_or_create(
                number=contract_number,
                date=contract_date,
                parent_user=customer,
            )
        except Exception as e:
            customer.delete()
            
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        seedlings = request.data.get('seedlings_list')
        try:
            for seedling in seedlings:
                seed_type = seedling.get('seedling_type')
                plant_status = seedling.get('plant_status')
                plant_date = seedling.get('plant_date')
                comment = seedling.get('comment')
            
                seedling, created = Seedling.objects.get_or_create(
                    seedling_type=SeedlingTypes.objects.get(id=seed_type),
                    plant_status=StatusTypes.objects.get(id=plant_status),
                    plant_date=plant_date,
                    comment=comment,
                    parent_contract=contract,
                )
        except Exception as e:
            contract.delete()
            customer.delete()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Record added successfully"})