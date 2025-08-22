from datetime import datetime
from typing import override
import base64
import io
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

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

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import get_user_model

# User = get_user_model()


from rest_framework import views, viewsets, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BindQRCodeView(views.APIView):
    @swagger_auto_schema(
        operation_description="Bind a QR code to a household",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['qr_code', 'household_id'],
            properties={
                'qr_code': openapi.Schema(type=openapi.TYPE_STRING, description='The QR code value to bind'),
                'household_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the household to bind the QR code to')
            }
        ),
        responses={
            200: openapi.Response(description='Successfully bound QR code to household'),
            400: openapi.Response(description='Invalid input data'),
            404: openapi.Response(description='QR code or household not found')
        }
    )
    def post(self, request):
        qr_code_value = request.data.get("qr_code")
        household_id = request.data.get("household_id")
        if not qr_code_value or not household_id:
            return Response({"error": "qr_code and household_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            qr_code = QrCode.objects.get(qr_code=qr_code_value)
        except QrCode.DoesNotExist:
            return Response({"error": "QR code not found"}, status=status.HTTP_404_NOT_FOUND)
        if qr_code.connected_household:
            return Response({"error": "QR code is already bound"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            household = Household.objects.get(id=household_id)
        except Household.DoesNotExist:
            return Response({"error": "Household not found"}, status=status.HTTP_404_NOT_FOUND)
        qr_code.connected_household = household
        qr_code.save()
        return Response({"message": "QR code successfully bound to household"}, status=status.HTTP_200_OK)

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
    @swagger_auto_schema(
        operation_description="Add a new record with household, customer, contract and seedlings information",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mahalla_id', 'street', 'house_number', 'fio', 'passport', 'birthday', 
                    'phone', 'contract_number', 'contract_date', 'seedlings_list'],
            properties={
                'mahalla_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the mahalla'),
                'street': openapi.Schema(type=openapi.TYPE_STRING, description='Street name'),
                'house_number': openapi.Schema(type=openapi.TYPE_STRING, description='House number'),
                'fio': openapi.Schema(type=openapi.TYPE_STRING, description='Full name of the customer'),
                'passport': openapi.Schema(type=openapi.TYPE_STRING, description='Passport number'),
                'birthday': openapi.Schema(type=openapi.FORMAT_DATE, description='Date of birth (YYYY-MM-DD)'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
                'contract_number': openapi.Schema(type=openapi.TYPE_STRING, description='Contract number'),
                'contract_date': openapi.Schema(type=openapi.FORMAT_DATE, description='Contract date (YYYY-MM-DD)'),
                'seedlings_list': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='List of seedlings to add',
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['seedling_type', 'plant_status', 'plant_date'],
                        properties={
                            'seedling_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the seedling type'),
                            'plant_status': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the plant status'),
                            'plant_date': openapi.Schema(type=openapi.FORMAT_DATE, description='Planting date (YYYY-MM-DD)'),
                            'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Optional comment')
                        }
                    )
                )
            }
        ),
        responses={
            201: openapi.Response(description='Record created successfully'),
            400: openapi.Response(description='Invalid input data'),
            403: openapi.Response(description='Permission denied')
        },
        tags=['Records']
    )
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
            for seedling_data in seedlings:
                seed_type = seedling_data.get('seedling_type')
                plant_status = seedling_data.get('plant_status')
                plant_date = seedling_data.get('plant_date')
                comment = seedling_data.get('comment', '')
                location = seedling_data.get('location', 'Not specified')
            
                seedling, created = Seedling.objects.get_or_create(
                    seedling_type=SeedlingTypes.objects.get(id=seed_type),
                    plant_status=StatusTypes.objects.get(id=plant_status),
                    plant_date=plant_date,
                    comment=comment,
                    location=location,
                    parent_contract=contract,
                )
        except Exception as e:
            contract.delete()
            customer.delete()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Record added successfully"})
    


class GetUserView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get current user information",
        responses={
            200: openapi.Response(
                description='User information',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email address')
                    }
                )
            ),
            401: openapi.Response(
                description='Authentication credentials were not provided or invalid',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            )
        },
        tags=['Users'],
        security=[{'Bearer': []}]
    )
    def get(self, request):
        try:
            # Get the authenticated user
            user = request.user
            
            # If user is not authenticated, return 401
            if not user.is_authenticated or user.is_anonymous:
                return Response(
                    {"detail": "Authentication credentials were not provided or are invalid."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Return user data
            return Response({
                "id": user.id,
                "username": user.username,
                "email": getattr(user, 'email', None)  # Safely get email attribute
            })
            
        except Exception as e:
            # Log the error for debugging
            print(f"Error in GetUserView: {str(e)}")
            return Response(
                {"detail": "An error occurred while processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserRecordsView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get all records created by the current user, optionally filtered by mahalla",
        manual_parameters=[
            openapi.Parameter(
                'mahalla_id',
                openapi.IN_QUERY,
                description='Optional ID of the mahalla to filter records',
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description='List of user records with household, customer and contract information',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'household': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description='Household information',
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'street': openapi.Schema(type=openapi.TYPE_STRING),
                                    'house': openapi.Schema(type=openapi.TYPE_STRING),
                                    'parent_mfy': openapi.Schema(type=openapi.TYPE_INTEGER)
                                }
                            ),
                            'customer': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description='Customer information',
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'fio': openapi.Schema(type=openapi.TYPE_STRING),
                                    'passport': openapi.Schema(type=openapi.TYPE_STRING),
                                    'birthday': openapi.Schema(type=openapi.FORMAT_DATE),
                                    'phone': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            ),
                            'contract': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description='Contract information',
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'contract_number': openapi.Schema(type=openapi.TYPE_STRING),
                                    'contract_date': openapi.Schema(type=openapi.FORMAT_DATE),
                                    'parent_user': openapi.Schema(type=openapi.TYPE_INTEGER)
                                }
                            )
                        }
                    )
                )
            ),
            400: openapi.Response(description='Invalid mahalla_id provided'),
            401: openapi.Response(description='Authentication credentials were not provided'),
            403: openapi.Response(description='User does not have permission to view records for this mahalla')
        },
        tags=['Records']
    )
    def get(self, request):
        user = request.user
        mahalla_id = request.query_params.get("mahalla_id")
        
        try:
            if mahalla_id:
                mahalla = Mahalla.objects.get(id=mahalla_id)
                user_records = Household.objects.filter(parent_mfy=mahalla, created_by=user)
            else:
                user_records = Household.objects.filter(created_by=user)
            
            result_list = []
            for record in user_records: 
                try:
                    # Get the first customer or None
                    customer = Customer.objects.filter(parent_household=record).first()
                    if not customer:
                        continue  # Skip if no customer exists
                        
                    contract = Contract.objects.filter(parent_user=customer).first()
                    if not contract:
                        continue  # Skip if no contract exists
                        
                    result_list.append({
                        "household": HouseholdSerializer(record).data,
                        "customer": CustomerSerializer(customer).data,
                        "contract": ContractSerializer(contract).data,
                    })
                except Exception as e:
                    # Log the error and continue with next record
                    print(f"Error processing household {record.id}: {str(e)}")
                    continue
                    
            return Response(result_list)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UnboundHouseholdsView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get households without a bound QR code created by the current user",
        responses={
            200: openapi.Response(
                description='List of households (id and name) without QR bound',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Household ID'),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Household display name'),
                        }
                    )
                )
            ),
        },
        tags=['Households']
    )
    def get(self, request):
        user = request.user
        mahalla_id = request.query_params.get("mahalla_id")
        
        try:
            if mahalla_id:
                mahalla = Mahalla.objects.get(id=mahalla_id)
                user_records = Household.objects.filter(parent_mfy=mahalla, created_by=user, qr_code__isnull=True)
            else:
                user_records = Household.objects.filter(created_by=user, qr_code__isnull=True)
            
            result_list = []
            for record in user_records: 
                try:
                    # Get the first customer or None
                    customer = Customer.objects.filter(parent_household=record).first()
                    if not customer:
                        continue  # Skip if no customer exists
                        
                    contract = Contract.objects.filter(parent_user=customer).first()
                    if not contract:
                        continue  # Skip if no contract exists
                        
                    result_list.append({
                        "household": HouseholdSerializer(record).data,
                        "customer": CustomerSerializer(customer).data,
                        "contract": ContractSerializer(contract).data,
                    })
                except Exception as e:
                    # Log the error and continue with next record
                    print(f"Error processing household {record.id}: {str(e)}")
                    continue
                    
            return Response(result_list)
                
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ContractSeedlingsView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get all seedlings for a specific contract",
        manual_parameters=[
            openapi.Parameter(
                'contract_id',
                openapi.IN_QUERY,
                description='ID of the contract to get seedlings for',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='List of seedlings for the contract',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Seedling ID'),
                            'seedling_type': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the seedling type'),
                            'plant_status': openapi.Schema(type=openapi.TYPE_STRING, description='Current status of the plant'),
                            'plant_date': openapi.Schema(type=openapi.FORMAT_DATE, description='Date when the seedling was planted'),
                            'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Optional comment about the seedling', nullable=True)
                        }
                    )
                )
            ),
            400: openapi.Response(
                description='Missing or invalid contract_id',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            ),
            401: openapi.Response(description='Authentication credentials were not provided'),
            403: openapi.Response(description='User does not have permission to view this contract'),
            404: openapi.Response(description='Contract not found')
        },
        tags=['Contracts', 'Seedlings']
    )
    def get(self, request):
        user = request.user
        contract_id = request.query_params.get("contract_id")
        if not contract_id:
            return Response(
                {"detail": "Contract id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            contract = Contract.objects.get(id=contract_id)
            # TODO: Add permission check if needed
            # if contract.parent_user.parent_household.created_by != user:
            #     return Response(
            #         {"detail": "You don't have permission to view this contract"}, 
            #         status=status.HTTP_403_FORBIDDEN
            #     )
                
            contract_seedlings = Seedling.objects.filter(parent_contract=contract)
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
            
        except Contract.DoesNotExist:
            return Response(
                {"detail": "Contract not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class CheckQRView(views.APIView):
    @swagger_auto_schema(
        operation_description="Check the status of a QR code and get associated data if bound",
        manual_parameters=[
            openapi.Parameter(
                'uuid',
                openapi.IN_QUERY,
                description='The UUID of the QR code to check',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='QR code status',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Status message'),
                        'code': openapi.Schema(type=openapi.TYPE_STRING, description='Status code'),
                        'household': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'street': openapi.Schema(type=openapi.TYPE_STRING),
                                'house_number': openapi.Schema(type=openapi.TYPE_STRING),
                                'fio': openapi.Schema(type=openapi.TYPE_STRING),
                                'phone': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        ),
                        'seedlings': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'seedling_type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'plant_status': openapi.Schema(type=openapi.TYPE_STRING),
                                    'plant_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                    'comment': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    }
                )
            ),
            400: openapi.Response(
                description='Invalid QR code',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                        'code': openapi.Schema(type=openapi.TYPE_STRING, description='Error code')
                    }
                )
            )
        }
    )
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
            customer = Customer.objects.filter(parent_household=household).first()
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
    @swagger_auto_schema(
        operation_description="Add agricultural events for seedlings",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['events_list'],
            properties={
                'events_list': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['seedling_id', 'status_id'],
                        properties={
                            'seedling_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the seedling'),
                            'status_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the status type'),
                            'date': openapi.Schema(type=openapi.FORMAT_DATE, description='Date of the event (YYYY-MM-DD)'),
                            'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Optional comment'),
                            'photo': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'base64': openapi.Schema(type=openapi.TYPE_STRING, description='Base64 encoded image data'),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the photo file')
                                }
                            )
                        }
                    )
                )
            }
        ),
        responses={
            200: openapi.Response(description='Successfully added agro events'),
            400: openapi.Response(description='Invalid input data')
        }
    )
    def post(self, request):
        try:
            events_list = request.data.get("events_list")
            if not events_list:
                return Response({"error": "events_list is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            for event in events_list:
                seedling_id = event.get("seedling_id")
                if not seedling_id:
                    return Response({"error": "seedling_id is required for each event"}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    seedling = Seedling.objects.get(id=seedling_id)
                except Seedling.DoesNotExist:
                    return Response({"error": f"Seedling with id {seedling_id} not found"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Create agro event
                try:
                    status_instance = StatusTypes.objects.get(id=event.get("status_id"))
                except StatusTypes.DoesNotExist:
                    return Response({"error": f"Status with id {event.get('status_id')} not found"}, status=status.HTTP_400_BAD_REQUEST)
                
                agro_event = AgroEvent.objects.create(
                    parent_seedling=seedling,
                    date=event.get("date") or timezone.now().date(),
                    comment=event.get("comment", ""),
                    status=status_instance
                )
                
                # Handle photo if provided
                photo_data = event.get("photo")
                if photo_data and photo_data.get("base64"):
                    try:
                        photo_base64 = photo_data.get("base64")
                        # Remove data URL prefix if present
                        if "," in photo_base64:
                            photo_base64 = photo_base64.split(",")[1]
                        
                        photo_binary = base64.b64decode(photo_base64)
                        photo_name = photo_data.get("name", f"agro_event_{agro_event.id}.jpg")
                        
                        # Create ContentFile from binary data
                        photo_file = ContentFile(photo_binary, name=photo_name)
                        
                        Photos.objects.create(
                            name=photo_name,
                            image=photo_file,
                            attached_to=agro_event,
                        )
                    except Exception as photo_error:
                        return Response({"error": f"Photo processing failed: {str(photo_error)}"}, status=status.HTTP_400_BAD_REQUEST)
                        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": "Agro events added successfully"}, status=status.HTTP_200_OK)


class SeedlingAgroEventsView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get all agro events for a specific seedling",
        manual_parameters=[
            openapi.Parameter(
                'seedling_id',
                openapi.IN_QUERY,
                description='ID of the seedling to get events for',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='List of agro events for the seedling',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Event ID'),
                            'date': openapi.Schema(type=openapi.FORMAT_DATE, description='Date of the event'),
                            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status name'),
                            'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Optional comment'),
                            'photo_url': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                description='URL to the photo if available',
                                nullable=True
                            )
                        }
                    )
                )
            ),
            400: openapi.Response(description='Missing or invalid seedling_id'),
            404: openapi.Response(description='Seedling not found')
        }
    )
    def get(self, request):
        seedling_id = request.query_params.get("seedling_id")
        if not seedling_id:
            return Response({"error": "seedling_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            seedling = Seedling.objects.get(id=seedling_id)
            agro_events = AgroEvent.objects.filter(parent_seedling=seedling).order_by('-date')
            
            result_list = []
            for event in agro_events:
                event_data = {
                    "id": event.id,
                    "date": event.date,
                    "comment": event.comment,
                    "status": event.status.name,
                    "photos": []
                }
                
                # Get photos for this event
                photos = Photos.objects.filter(attached_to=event)
                for photo in photos:
                    event_data["photos"].append({
                        "id": photo.id,
                        "name": photo.name,
                        "image_url": photo.image.url if photo.image else None
                    })
                
                result_list.append(event_data)
            
            return Response({
                "seedling_id": seedling_id,
                "agro_events": result_list
            }, status=status.HTTP_200_OK)
            
        except Seedling.DoesNotExist:
            return Response({"error": f"Seedling with id {seedling_id} not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
      
        
