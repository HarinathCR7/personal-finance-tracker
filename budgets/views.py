from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render
from transactions.models import Transaction
from .models import Budget, BudgetAlert
from .serializers import BudgetSerializer, BudgetAlertSerializer

def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        budget = self.get_object()
        today = timezone.now().date()

        # Get transactions for the budget period
        transactions = Transaction.objects.filter(
            category=budget.category,
            transaction_type='EXPENSE',
            date__range=[budget.start_date, budget.end_date]
        )

        total_spent = transactions.aggregate(total=Sum('amount'))['total'] or 0
        remaining = budget.amount - total_spent
        percentage_used = (total_spent / budget.amount * 100) if budget.amount > 0 else 0

        # Check alerts
        alerts = []
        for alert in budget.alerts.filter(is_active=True):
            if alert.alert_type == 'PERCENTAGE' and percentage_used >= alert.threshold:
                alerts.append(f"Budget usage reached {percentage_used:.1f}%")
            elif alert.alert_type == 'AMOUNT' and remaining <= alert.threshold:
                alerts.append(f"Remaining budget is ${remaining:.2f}")

        return Response({
            'budget': budget.amount,
            'total_spent': total_spent,
            'remaining': remaining,
            'percentage_used': percentage_used,
            'alerts': alerts
        })

class BudgetAlertViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetAlertSerializer
    queryset = BudgetAlert.objects.all()

    def perform_create(self, serializer):
        budget_id = self.request.data.get('budget')
        budget = Budget.objects.get(id=budget_id)
        serializer.save(budget=budget) 