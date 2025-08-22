from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

# Common parameters
QR_CODE_PARAM = openapi.Parameter(
    'qr_code', 
    openapi.IN_QUERY, 
    description="QR code identifier", 
    type=openapi.TYPE_STRING,
    required=True
)

# Request/Response schemas
class ErrorResponse(serializers.Serializer):
    error = serializers.CharField()
    details = serializers.DictField(required=False)

class AgroEventRequest(serializers.Serializer):
    seedling_id = serializers.IntegerField(required=True)
    event_type = serializers.CharField(required=True)
    event_date = serializers.DateField(required=True)
    comment = serializers.CharField(required=False, allow_blank=True)
    photo = serializers.ImageField(required=False)

# Decorators for views
def bind_qr_code_docs():
    return swagger_auto_schema(
        operation_description="Bind a QR code to a seedling",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['qr_code', 'seedling_id'],
            properties={
                'qr_code': openapi.Schema(type=openapi.TYPE_STRING),
                'seedling_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={
            200: 'QR code successfully bound',
            400: 'Invalid input',
            404: 'QR code or seedling not found'
        }
    )

def custom_add_record_docs():
    return swagger_auto_schema(
        operation_description="Add a new record with customer, household, contract, and seedling information",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mahalla_id', 'street', 'house_number', 'fio', 'passport', 'phone', 'contract_number', 'contract_date', 'seedlings_list'],
            properties={
                'mahalla_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the mahalla'),
                'street': openapi.Schema(type=openapi.TYPE_STRING, description='Street name'),
                'house_number': openapi.Schema(type=openapi.TYPE_STRING, description='House number'),
                'fio': openapi.Schema(type=openapi.TYPE_STRING, description='Full name of the customer'),
                'passport': openapi.Schema(type=openapi.TYPE_STRING, description='Passport number'),
                'birthday': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Date of birth (YYYY-MM-DD)'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
                'contract_number': openapi.Schema(type=openapi.TYPE_STRING, description='Contract number'),
                'contract_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Contract date (YYYY-MM-DD)'),
                'seedlings_list': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['seedling_type', 'plant_status'],
                        properties={
                            'seedling_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the seedling type'),
                            'plant_status': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the plant status'),
                            'plant_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Planting date (YYYY-MM-DD)'),
                            'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Additional comments')
                        }
                    )
                )
            }
        ),
        responses={
            201: 'Record created successfully',
            400: 'Invalid input data',
            404: 'Mahalla not found'
        }
    )

def add_agro_event_docs():
    return swagger_auto_schema(
        operation_description="Add a new agricultural event for a seedling",
        request_body=AgroEventRequest,
        responses={
            201: 'Event added successfully',
            400: 'Invalid input data',
            404: 'Seedling not found'
        }
    )

def seedling_agro_events_docs():
    return swagger_auto_schema(
        operation_description="Get all agricultural events for a specific seedling",
        manual_parameters=[
            openapi.Parameter(
                'seedling_id',
                openapi.IN_QUERY,
                description="ID of the seedling",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: AgroEventSerializer(many=True),
            400: 'Invalid input data',
            404: 'Seedling not found'
        }
    )

def check_qr_docs():
    return swagger_auto_schema(
        operation_description="Check and retrieve information about a QR code",
        manual_parameters=[QR_CODE_PARAM],
        responses={
            200: 'QR code information',
            400: 'QR code not provided',
            404: 'QR code not found'
        }
    )

def contract_seedlings_docs():
    return swagger_auto_schema(
        operation_description="Get all seedlings for a specific contract",
        manual_parameters=[
            openapi.Parameter(
                'contract_id',
                openapi.IN_QUERY,
                description="ID of the contract",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: SeedlingSerializer(many=True),
            400: 'Contract ID not provided',
            404: 'Contract not found'
        }
    )

def user_records_docs():
    return swagger_auto_schema(
        operation_description="Get all records for the current user",
        responses={
            200: 'List of user records',
            401: 'User not authenticated'
        }
    )

def get_user_docs():
    return swagger_auto_schema(
        operation_description="Get information about the current user",
        responses={
            200: UserSerializer(),
            401: 'User not authenticated'
        }
    )
