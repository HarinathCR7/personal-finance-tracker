<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Budget, BudgetAlert
from .forms import BudgetForm
from transactions.models import Transaction, Category

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    alerts = BudgetAlert.objects.filter(budget__user=request.user, is_read=False)
    
    # Calculate current spending for each budget
    for budget in budgets:
        transactions = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            date__range=[budget.start_date, budget.end_date],
            type='EXPENSE'
        )
        current_spending = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        budget.current_spending = current_spending
        budget.remaining = budget.amount - current_spending
        budget.percentage_used = (current_spending / budget.amount * 100) if budget.amount > 0 else 0
    
    return render(request, 'budgets/budget_list.html', {
        'budgets': budgets,
        'alerts': alerts
    })

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('budget_list')
    else:
        form = BudgetForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
    
    return render(request, 'budgets/budget_form.html', {'form': form, 'action': 'Create'})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
    
    return render(request, 'budgets/budget_form.html', {'form': form, 'action': 'Update'})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('budget_list')
    return render(request, 'budgets/budget_confirm_delete.html', {'budget': budget})

@login_required
def mark_alert_read(request, pk):
    alert = get_object_or_404(BudgetAlert, pk=pk, budget__user=request.user)
    alert.is_read = True
    alert.save()
    messages.success(request, 'Alert marked as read.')
    return redirect('budget_list') 
>>>>>>> 98821739fc61ab0cfe2950074ca42dcf5f9c9704
