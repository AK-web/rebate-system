from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import RebateProgram, Transaction, RebateClaim
from .serializers import (
    RebateProgramSerializer, 
    TransactionSerializer, 
    RebateClaimSerializer, 
    RebateReportSerializer
)
from django.core.cache import cache

# Create Rebate Program
class CreateRebateProgram(APIView):
    """
    Endpoint to create a new rebate program.
    """
    def post(self, request):
        serializer = RebateProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Submit Transaction
class SubmitTransaction(APIView):
    """
    Endpoint to submit a new transaction.
    """
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Calculate Rebate
class CalculateRebate(APIView):
    """
    Endpoint to calculate the rebate amount for a given transaction.
    """
    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            rebate_amount = transaction.calculate_rebate_amount()
            return Response({"transaction_id": transaction_id, "rebate_amount": rebate_amount}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

# Claim Rebate
class ClaimRebate(APIView):
    """
    Endpoint to create a rebate claim and mark it as 'pending'.
    """
    def post(self, request):
        serializer = RebateClaimSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = serializer.validated_data['transaction'].transaction_id
            if not Transaction.objects.filter(transaction_id=transaction_id).exists():
                return Response({"error": "Transaction does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Automatically assign claim_amount if not provided
            if not serializer.validated_data.get('claim_amount'):
                claim_amount = serializer.validated_data['transaction'].calculate_rebate_amount()
                serializer.validated_data['claim_amount'] = claim_amount
            
            serializer.save(claim_status='pending')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Rebate Report
class RebateReport(APIView):
    """
    Endpoint to generate a summary report of rebate claims within a given time period.
    """
    def post(self, request):
        serializer = RebateReportSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            # Generate a unique cache key based on the request parameters
            cache_key = f"rebate_report_{start_date}_{end_date}"

            # Try to get the report from the cache
            cached_report = cache.get(cache_key)
            if cached_report:
                return Response(cached_report, status=status.HTTP_200_OK)

            # If not found in cache, generate the report
            claims = RebateClaim.objects.filter(claim_date__range=[start_date, end_date])
            total_claims = claims.count()
            total_approved_amount = claims.filter(claim_status='approved').aggregate(Sum('claim_amount'))['claim_amount__sum'] or 0

            report_data = {
                "total_claims": total_claims,
                "total_approved_amount": total_approved_amount
            }

            # Cache the result for 10 minutes (600 seconds)
            cache.set(cache_key, report_data, timeout=600)

            return Response(report_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)