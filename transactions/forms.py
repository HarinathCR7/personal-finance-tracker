from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['category'].queryset = Category.objects.filter(user=kwargs['instance'].user)
        elif 'initial' in kwargs and 'user' in kwargs['initial']:
            self.fields['category'].queryset = Category.objects.filter(user=kwargs['initial']['user'])

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        } 