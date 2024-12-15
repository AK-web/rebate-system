from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import RebateProgram, Transaction, RebateClaim

@admin.register(RebateProgram)
class RebateProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name', 'rebate_percentage', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('program_name', 'eligibility_criteria')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'amount', 'transaction_date', 'rebate_program')
    list_filter = ('transaction_date', 'rebate_program')
    search_fields = ('transaction_id',)

@admin.register(RebateClaim)
class RebateClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id', 'transaction', 'claim_amount', 'claim_status', 'claim_date')
    list_filter = ('claim_status', 'claim_date')
    search_fields = ('claim_id', 'transaction__transaction_id')