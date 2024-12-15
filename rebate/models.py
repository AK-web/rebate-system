from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  


class RebateProgram(models.Model):
    """
    Model representing a rebate program with its details and eligibility criteria.
    """
    program_name = models.CharField(
        max_length=200, 
        unique=True, 
        help_text="Unique name of the rebate program"
    )
    rebate_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of rebate offered (0-100%)"
    )
    start_date = models.DateField(help_text="Start date of the rebate program")
    end_date = models.DateField(help_text="End date of the rebate program")
    eligibility_criteria = models.TextField(blank=True, null=True, help_text="Detailed description of program eligibility")
    is_active = models.BooleanField(default=True, help_text="Whether the rebate program is currently active")

    def __str__(self):
        return f"{self.program_name} ({self.start_date} to {self.end_date})"

    def is_valid_now(self):
        """
        Check if the rebate program is currently valid
        """
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date

    class Meta:
        verbose_name_plural = "Rebate Programs"
        ordering = ['-start_date']


class Transaction(models.Model):
    """
    Model representing a transaction eligible for rebate.
    """
    transaction_id = models.CharField(
        max_length=100, 
        unique=True, 
        help_text="Unique identifier for the transaction"
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Total transaction amount"
    )
    transaction_date = models.DateTimeField(help_text="Date and time of the transaction")
    rebate_program = models.ForeignKey(
        RebateProgram, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='transactions',
        help_text="Rebate program associated with this transaction"
    )
    

    def __str__(self):
        return f"Transaction {self.transaction_id} - ${self.amount}"

    def calculate_rebate_amount(self):
        """
        Calculate the rebate amount based on the associated program
        """
        if self.rebate_program and self.rebate_program.is_valid_now():
            return self.amount * (self.rebate_program.rebate_percentage / 100)
        return 0
        

    def clean(self):
        """
        Custom validation to ensure the transaction date is within the rebate program's valid date range.
        """
        if self.rebate_program:
            if self.transaction_date.date() < self.rebate_program.start_date or self.transaction_date.date() > self.rebate_program.end_date:
                raise ValidationError(_(
                    "Transaction date must be within the start and end dates of the associated rebate program."
                ))

    def save(self, *args, **kwargs):
        """
        Override save method to validate before saving.
        """
        self.clean()  # Enforce validation rules
        super().save(*args, **kwargs)  # Call the parent save method


    class Meta:
        verbose_name_plural = "Transactions"
        ordering = ['-transaction_date']


class RebateClaim(models.Model):
    """
    Model representing a rebate claim for a specific transaction.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    claim_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Unique identifier for the rebate claim"
    )

    # Using OneToOneField to ensure one claim per transaction
    transaction = models.OneToOneField(
        Transaction, 
        on_delete=models.CASCADE, 
        related_name='rebate_claim', 
        help_text="Transaction associated with this claim"
    )
    
    claim_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Amount of rebate claimed"
    )
    
    claim_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text="Current status of the rebate claim"
    )
    
    claim_date = models.DateTimeField(
        auto_now_add=True, 
        help_text="Date and time when the claim was submitted"
    )
    
    notes = models.TextField(
        blank=True, 
        null=True, 
        help_text="Additional notes or reason for claim status"
    )

    def __str__(self):
        return f"Claim {self.claim_id} - {self.claim_status}"

    def clean(self):  # Added custom validation
        """
        Custom validation to ensure no duplicate claims are created for the same transaction.
        """
        if RebateClaim.objects.filter(transaction=self.transaction).exclude(pk=self.pk).exists():
            raise ValidationError(_("A rebate claim already exists for this transaction."))  # Raise error if duplicate

    def save(self, *args, **kwargs):
        """
        Override save method to ensure claim amount matches transaction rebate 
        and prevent duplicate rebate claims for a transaction.
        """
        self.clean() 
        if not self.claim_amount:
            self.claim_amount = self.transaction.calculate_rebate_amount()

        # Ensure only one rebate claim can be created per transaction
        # The OneToOneField will prevent multiple claims, so no need for additional validation here
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Rebate Claims"
        ordering = ['-claim_date']
