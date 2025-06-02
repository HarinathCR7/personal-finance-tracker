from rest_framework import serializers
from .models import Budget, BudgetAlert
from transactions.serializers import CategorySerializer

class BudgetAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetAlert
        fields = ['id', 'alert_type', 'threshold', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class BudgetSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    alerts = BudgetAlertSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = [
            'id', 'category', 'category_details', 'amount',
            'period', 'start_date', 'end_date', 'alerts',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data 