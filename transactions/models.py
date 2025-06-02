from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.type} - {self.amount} - {self.date}"
    
    class Meta:
        ordering = ['-date'] 