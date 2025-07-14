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
    CustomUser,
    QrCode,

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
        """ example_request_body
        {
            "mahalla_id": 1,
            "street": "Street",
            "house_number": "House Number",
            "fio": "FIO",
            "passport": "Passport",
            "birthday": "Birthday",
            "phone": "Phone",
            "contract_number": "Contract Number",
            "contract_date": "Contract Date",
            "seedlings_list": [
                {
                    "seedling_type": 1,
                    "plant_status": 1,
                    "plant_date": "Plant Date",
                    "comment": "Comment"
                }
            ]
        }
        
        """
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
    
class GetUserView(views.APIView):
    def get(self, request):
        user = request.user
        return Response({"user": UserSerializer(user).data['username']})

class UserRecordsView(views.APIView):
    def get(self, request):
        user = request.user
        mahalla_id = request.data.get("mahalla_id")
        if mahalla_id:
            mahalla = Mahalla.objects.get(id=mahalla_id)
            user_records = Household.objects.filter(parent_mfy=mahalla, created_by=user)
        else:
            user_records = Household.objects.filter(created_by=user)
        result_list = []
        for record in user_records: 
            customer = Customer.objects.get(parent_household=record)
            contract = Contract.objects.get(parent_user=customer)
            result_list.append({
                "household": HouseholdSerializer(record).data,
                "customer": CustomerSerializer(customer).data,
                "contract": ContractSerializer(contract).data,
            })
        return Response(result_list)

class ContractSeedlingsView(views.APIView):
    def get(self, request):
        #TODO: add user check
        user = request.user
        contract_id = request.query_params.get("contract_id")
        if contract_id:
            contract = Contract.objects.get(id=contract_id)
            contract_seedlings = Seedling.objects.filter(parent_contract=contract)
        else:
            return Response("Contract id is required", status=status.HTTP_400_BAD_REQUEST)
        result_list = []
        for seedling in contract_seedlings:
            result_list.append(
                {
                    "id": seedling.id,
                    "seedling_type": seedling.seedling_type.name,
                    "plant_status": seedling.plant_status.name,
                    "plant_date": seedling.plant_date,
                    "comment": seedling.comment,
                }
            )
        return Response(result_list)

class CheckQRView(views.APIView):
    def get(self, request):
        qr_id = request.query_params.get("uuid")
        try:
            qr_code = QrCode.objects.get(qr_code=qr_id)
        except QrCode.DoesNotExist:
            return Response({"message": "QR code not found", "code": "800"}, status=status.HTTP_400_BAD_REQUEST)
        except QrCode.MultipleObjectsReturned:
            return Response({"message": "Multiple QR codes found", "code": "801"}, status=status.HTTP_400_BAD_REQUEST)

        if not qr_code.connected_household:
            return Response({"message": "QR code is free to bind", "code": "700"}, status=status.HTTP_200_OK)
        elif qr_code.connected_household.created_by != request.user:
            return Response({"message": "QR code is not connected to your household", "code": "801"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            household = qr_code.connected_household
            customer = Customer.objects.get(parent_household=household)
            contract = Contract.objects.get(parent_user=customer)
            seedlings = Seedling.objects.filter(parent_contract=contract)
            result_list = []
            for seedling in seedlings:
                result_list.append(
                    {
                        "id": seedling.id,
                        "seedling_type": seedling.seedling_type.name,
                        "plant_status": seedling.plant_status.name,
                        "plant_date": seedling.plant_date,
                        "comment": seedling.comment,
                    }
                )
            response = {
                "message": "QR code is connected to your household",
                "code": "701",
                "data": {
                    "household": HouseholdSerializer(household).data,
                    "customer": CustomerSerializer(customer).data,
                    "contract": ContractSerializer(contract).data,
                    "seedlings": result_list,
                }
            }
            return Response(response, status=status.HTTP_200_OK)


class AddAgroEventView(views.APIView):
    def post(self, request):
        events_list = request.data.get("events_list")
        for event in events_list:
            seedling_id = event.get("seedling_id")
            seedling = Seedling.objects.get(id=seedling_id)
            agro_event = AgroEvent.objects.create(
                parent_seedling=seedling,
                date=event.get("date"),
                comment=event.get("comment"),
            )
            agro_event.status = StatusTypes.objects.get(id=event.get("status_id"))
            photo_base64 = event.get("photo").get("base64")
            photo = base64.b64decode(photo_base64)
            agro_event.save()
            photos = Photos.objects.create(
                attached_to=agro_event,
                photo=photo,
            )
        return Response({"message": "Agro events added successfully"}, status=status.HTTP_200_OK)
            
      
        
