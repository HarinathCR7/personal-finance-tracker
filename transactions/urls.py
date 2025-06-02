<<<<<<< HEAD
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
=======
from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('<int:pk>/update/', views.transaction_update, name='transaction_update'),
    path('<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
>>>>>>> 98821739fc61ab0cfe2950074ca42dcf5f9c9704
] 