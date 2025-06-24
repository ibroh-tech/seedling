"""
URL configuration for seedling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
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
)

router = routers.DefaultRouter()
router.register(r'agroevents', AgroEventViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'users', UserViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'households', HouseholdViewSet)
router.register(r'mahallas', MahallaViewSet)
router.register(r'photos', PhotosViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'seedlings', SeedlingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
