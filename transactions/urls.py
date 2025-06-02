from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'transactions'

router = DefaultRouter()
router.register(r'transactions', views.TransactionViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('add-category/', views.add_category, name='add_category'),
    path('api/', include(router.urls)),
] 