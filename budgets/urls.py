from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'budgets', views.BudgetViewSet, basename='budget')
router.register(r'alerts', views.BudgetAlertViewSet, basename='budgetalert')

app_name = 'budgets'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.budget_list, name='budget_list'),
] 