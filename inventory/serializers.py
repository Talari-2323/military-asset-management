from rest_framework import serializers
from .models import Base, EquipmentType, Purchase, Transfer, Assignment, Expenditure

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = "__all__"

class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = "__all__"

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"
        read_only_fields = ["assigned_by"]

class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        fields = "__all__"
        read_only_fields = ["recorded_by"]
