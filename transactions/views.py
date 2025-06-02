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