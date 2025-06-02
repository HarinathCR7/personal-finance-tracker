from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from transactions.models import Transaction
from django.db.models.functions import TruncMonth

@login_required
def home(request):
    # Get current month's start and end dates
    today = timezone.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    month_end = next_month - timedelta(days=1)

    # Get transactions for current month
    transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[month_start, month_end]
    )

    # Calculate totals
    total_income = transactions.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses

    # Get recent transactions
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]

    # Get category data for pie chart
    category_data = transactions.filter(type='EXPENSE').values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')

    category_labels = [item['category__name'] for item in category_data]
    category_values = [float(item['total']) for item in category_data]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'category_labels': category_labels,
        'category_data': category_values,
    }

    return render(request, 'home.html', context) 