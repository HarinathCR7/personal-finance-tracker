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