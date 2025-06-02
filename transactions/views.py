from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer
from .forms import TransactionForm, CategoryForm

@login_required
def transaction_list(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transactions:transaction_list')
    else:
        form = TransactionForm()
    
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'transactions': transactions,
        'form': form,
        'categories': categories,
    }
    return render(request, 'transactions/transaction_list.html', context)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('transactions:transaction_list')
    else:
        form = CategoryForm()
    return render(request, 'transactions/add_category.html', {'form': form})

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    queryset = Category.objects.all()

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']
    queryset = Transaction.objects.all()

    @action(detail=False, methods=['get'])
    def summary(self, request):
        period = request.query_params.get('period', 'month')
        today = timezone.now().date()

        if period == 'month':
            start_date = today.replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        else:  # year
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)

        transactions = self.get_queryset().filter(date__range=[start_date, end_date])
        
        income = transactions.filter(transaction_type='INCOME').aggregate(
            total=Sum('amount'))['total'] or 0
        expenses = transactions.filter(transaction_type='EXPENSE').aggregate(
            total=Sum('amount'))['total'] or 0

        category_summary = transactions.filter(transaction_type='EXPENSE').values(
            'category__name').annotate(total=Sum('amount'))

        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'total_income': income,
            'total_expenses': expenses,
            'net_savings': income - expenses,
            'category_summary': category_summary
        }) 