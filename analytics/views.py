from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from transactions.models import Transaction
from budgets.models import Budget

# Create your views here.

@login_required
def dashboard(request):
    # Get date range for current month
    today = timezone.now().date()
    start_date = today.replace(day=1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Get transactions for the current month
    transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )

    # Calculate totals
    total_income = transactions.filter(transaction_type='INCOME').aggregate(
        total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(transaction_type='EXPENSE').aggregate(
        total=Sum('amount'))['total'] or 0
    net_savings = total_income - total_expenses

    # Get category distribution
    category_summary = transactions.filter(transaction_type='EXPENSE').values(
        'category__name').annotate(total=Sum('amount'))
    
    category_labels = [item['category__name'] for item in category_summary]
    category_data = [float(item['total']) for item in category_summary]

    # Get recent transactions
    recent_transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')[:10]

    # Get budget status
    budgets = Budget.objects.filter(user=request.user)
    budget_status = "On Track"
    for budget in budgets:
        spent = transactions.filter(
            category=budget.category,
            transaction_type='EXPENSE'
        ).aggregate(total=Sum('amount'))['total'] or 0
        if spent > budget.amount:
            budget_status = "Over Budget"
            break

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_savings': net_savings,
        'category_labels': category_labels,
        'category_data': category_data,
        'recent_transactions': recent_transactions,
        'budget_status': budget_status,
    }
    
    return render(request, 'analytics/dashboard.html', context)
