from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Base, EquipmentType, Purchase, Transfer, Assignment, Expenditure
from .serializers import (
    BaseSerializer, EquipmentTypeSerializer, PurchaseSerializer,
    TransferSerializer, AssignmentSerializer, ExpenditureSerializer
)

class BaseViewSet(viewsets.ModelViewSet):
    queryset = Base.objects.all()
    serializer_class = BaseSerializer

class EquipmentTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all().order_by("-purchase_date")
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all().order_by("-transfer_date")
    serializer_class = TransferSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by("-assigned_date")
    serializer_class = AssignmentSerializer

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class ExpenditureViewSet(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all().order_by("-expenditure_date")
    serializer_class = ExpenditureSerializer

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

class DashboardView(APIView):
    def get(self, request):
        base_id = request.query_params.get("base")
        equipment_id = request.query_params.get("equipment")

        purchases = Purchase.objects.all()
        transfers_in = Transfer.objects.all()
        transfers_out = Transfer.objects.all()
        assignments = Assignment.objects.all()
        expenditures = Expenditure.objects.all()

        if base_id:
            purchases = purchases.filter(base_id=base_id)
            transfers_in = transfers_in.filter(to_base_id=base_id)
            transfers_out = transfers_out.filter(from_base_id=base_id)
            assignments = assignments.filter(base_id=base_id)
            expenditures = expenditures.filter(base_id=base_id)

        if equipment_id:
            purchases = purchases.filter(equipment_type_id=equipment_id)
            transfers_in = transfers_in.filter(equipment_type_id=equipment_id)
            transfers_out = transfers_out.filter(equipment_type_id=equipment_id)
            assignments = assignments.filter(equipment_type_id=equipment_id)
            expenditures = expenditures.filter(equipment_type_id=equipment_id)

        def total(qs):
            return qs.aggregate(total=Sum("quantity"))["total"] or 0

        purchase_total = total(purchases)
        transfer_in_total = total(transfers_in)
        transfer_out_total = total(transfers_out)
        assigned_total = total(assignments)
        expended_total = total(expenditures)
        net_movement = purchase_total + transfer_in_total - transfer_out_total

        return Response({
            "opening_balance": 0,
            "purchases": purchase_total,
            "transfer_in": transfer_in_total,
            "transfer_out": transfer_out_total,
            "net_movement": net_movement,
            "assigned": assigned_total,
            "expended": expended_total,
            "closing_balance": net_movement - assigned_total - expended_total,
        })
