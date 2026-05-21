from django.db import models
from django.contrib.auth.models import User


class RecoveryCase(models.Model):

    STATUS_CHOICES = [

        ('Customer Payment', 'Customer Payment'),
        ('Godowned', 'Godowned'),
        ('Released', 'Released'),

    ]

    vehicle_number = models.CharField(max_length=20)

    customer_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=15)

    customer_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    agent_name = models.CharField(max_length=100)

    agent_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    recovery_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES
    )

    remarks = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.customer_name