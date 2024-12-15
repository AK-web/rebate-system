from rest_framework import serializers
from .models import RebateProgram, Transaction, RebateClaim

class RebateProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = RebateProgram
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    rebate_amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_rebate_amount(self, obj):
        return obj.calculate_rebate_amount()

class RebateClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = RebateClaim
        fields = '__all__'

class RebateReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
