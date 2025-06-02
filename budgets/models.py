<<<<<<< HEAD
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from transactions.models import Category

class Budget(models.Model):
    PERIOD_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='MONTHLY')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'category', 'period', 'start_date')

    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.period})"

class BudgetAlert(models.Model):
    ALERT_TYPES = [
        ('PERCENTAGE', 'Percentage'),
        ('AMOUNT', 'Amount'),
    ]

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    threshold = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.budget.category.name} - {self.alert_type} Alert" 
=======
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from transactions.models import Category

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.category.name} - {self.amount}"
    
    class Meta:
        ordering = ['-start_date']

class BudgetAlert(models.Model):
    ALERT_TYPES = [
        ('WARNING', 'Warning'),
        ('EXCEEDED', 'Exceeded'),
    ]
    
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=8, choices=ALERT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.alert_type} - {self.budget.category.name}"
    
    class Meta:
        ordering = ['-created_at'] 
>>>>>>> 98821739fc61ab0cfe2950074ca42dcf5f9c9704
