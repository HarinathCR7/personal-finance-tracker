<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form, 'action': 'Add'})

@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/transaction_form.html', {'form': form, 'action': 'Update'})

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'transactions/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'transactions/category_form.html', {'form': form, 'action': 'Add'})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'transactions/category_form.html', {'form': form, 'action': 'Update'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'transactions/category_confirm_delete.html', {'category': category}) 
>>>>>>> 98821739fc61ab0cfe2950074ca42dcf5f9c9704
