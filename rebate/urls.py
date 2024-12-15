from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CreateRebateProgram, 
    SubmitTransaction, 
    CalculateRebate, 
    ClaimRebate, 
    RebateReport
)

# Create a router and register our viewsets with it
# router = DefaultRouter()
# router.register(r'rebate-programs', RebateProgramViewSet)
# router.register(r'transactions', TransactionViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    # path('', include(router.urls)),
    path('create-rebate-program/', CreateRebateProgram.as_view(), name='create_rebate_program'),
    path('submit-transaction/', SubmitTransaction.as_view(), name='submit_transaction'),
    path('calculate-rebate/<str:transaction_id>/', CalculateRebate.as_view(), name='calculate_rebate'),
    # path('calculate-rebate/<int:pk>/', CalculateRebate.as_view(), name='calculate_rebate'),
    path('claim-rebate/', ClaimRebate.as_view(), name='claim_rebate'),
    path('rebate-report/', RebateReport.as_view(), name='rebate_report'),
]