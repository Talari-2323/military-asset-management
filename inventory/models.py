from django.db import models
from django.contrib.auth.models import User

class Base(models.Model):
    name = models.CharField(max_length=120, unique=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class EquipmentType(models.Model):
    CATEGORY_CHOICES = [
        ("WEAPON", "Weapon"),
        ("VEHICLE", "Vehicle"),
        ("AMMUNITION", "Ammunition"),
        ("OTHER", "Other"),
    ]
    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=40, default="Units")

    def __str__(self):
        return self.name

class Purchase(models.Model):
    base = models.ForeignKey(Base, on_delete=models.PROTECT)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateField()
    reference_number = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

class Transfer(models.Model):
    from_base = models.ForeignKey(Base, on_delete=models.PROTECT, related_name="transfers_out")
    to_base = models.ForeignKey(Base, on_delete=models.PROTECT, related_name="transfers_in")
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    transfer_date = models.DateTimeField()
    status = models.CharField(max_length=30, default="COMPLETED")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

class Assignment(models.Model):
    base = models.ForeignKey(Base, on_delete=models.PROTECT)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT)
    personnel_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()
    assigned_date = models.DateField()
    assigned_by = models.ForeignKey(User, on_delete=models.PROTECT)

class Expenditure(models.Model):
    base = models.ForeignKey(Base, on_delete=models.PROTECT)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    expenditure_date = models.DateField()
    reason = models.CharField(max_length=250)
    recorded_by = models.ForeignKey(User, on_delete=models.PROTECT)

class AuditLog(models.Model):
    ACTIONS = [
        ("LOGIN", "Login"), ("CREATE", "Create"), ("UPDATE", "Update"),
        ("DELETE", "Delete"), ("PURCHASE", "Purchase"), ("TRANSFER", "Transfer"),
        ("ASSIGN", "Assign"), ("EXPEND", "Expend"),
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    action = models.CharField(max_length=30, choices=ACTIONS)
    module = models.CharField(max_length=80)
    record_id = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
