from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BaseViewSet, EquipmentTypeViewSet, PurchaseViewSet,
    TransferViewSet, AssignmentViewSet, ExpenditureViewSet, DashboardView
)

router = DefaultRouter()
router.register("bases", BaseViewSet)
router.register("equipment", EquipmentTypeViewSet)
router.register("purchases", PurchaseViewSet)
router.register("transfers", TransferViewSet)
router.register("assignments", AssignmentViewSet)
router.register("expenditures", ExpenditureViewSet)

urlpatterns = [
    path("dashboard/", DashboardView.as_view()),
    path("", include(router.urls)),
]
