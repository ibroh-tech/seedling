"""
URL configuration for seedling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

from seedling_app.views import (
    AgroEventViewSet,
    ContractViewSet,
    UserViewSet,
    CustomerViewSet,
    DistrictViewSet,
    HouseholdViewSet,
    MahallaViewSet,
    PhotosViewSet,
    RegionViewSet,
    SeedlingViewSet,
    StatusTypesViewSet,
    SeedlingTypesViewSet,
    CustomAddRecordView,
    AddAgroEventView,
    GetUserView,
    UserRecordsView,
    ContractSeedlingsView,
    CheckQRView,
    BindQRCodeView,
    UnboundHouseholdsView,
    SeedlingAgroEventsView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Schema View for API documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Seedling Backend API",
      default_version='v1',
      description="API documentation for Seedling Backend",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[],  # Disable authentication for schema view
   urlconf='seedling.urls',
)

router = routers.DefaultRouter()
# router.register(r'agroevents', AgroEventViewSet)
# router.register(r'contracts', ContractViewSet)
# router.register(r'users', UserViewSet)
# router.register(r'customers', CustomerViewSet)
# router.register(r'districts', DistrictViewSet)
# router.register(r'households', HouseholdViewSet)
router.register(r'mahallas', MahallaViewSet, basename="mahalla")
# router.register(r'photos', PhotosViewSet)
# router.register(r'regions', RegionViewSet)
# router.register(r'seedlings', SeedlingViewSet)
router.register(r'status_types', StatusTypesViewSet, basename="status_types")
router.register(r'seedling_types', SeedlingTypesViewSet, basename="seedling_types")

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API Endpoints
    path('api/', include(router.urls)),
    path('api/add-record/', CustomAddRecordView.as_view(), name='add-record'),
    path('api/add-agro-event/', AddAgroEventView.as_view(), name='add-agro-event'),
    path('api/get-user/', GetUserView.as_view(), name='get-user'),
    path('api/user-records/', UserRecordsView.as_view(), name='user-records'),
    path('api/contract-seedlings/', ContractSeedlingsView.as_view(), name='contract-seedlings'),
    path('api/check-qr/', CheckQRView.as_view(), name='check-qr'),
    path('api/bind-qr-code/', BindQRCodeView.as_view(), name='bind-qr-code'),
    path('api/unbound-households/', UnboundHouseholdsView.as_view(), name='unbound-households'),
    path('api/seedling-agro-events/', SeedlingAgroEventsView.as_view(), name='seedling-agro-events'),
    
    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
        schema_view.without_ui(cache_timeout=0), 
        name='schema-json'
    ),
    path('swagger/', 
        schema_view.with_ui('swagger', cache_timeout=0), 
        name='schema-swagger-ui'
    ),
    path('redoc/', 
        schema_view.with_ui('redoc', cache_timeout=0), 
        name='schema-redoc'
    ),
    path('openapi.json', 
        schema_view.without_ui(cache_timeout=0), 
        name='schema-json-raw',
        kwargs={'format': '.json'}
    ),
    # Add favicon.ico handler
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
