from django.urls import path
from .views import index, CustomerViewset,ProductViewset

urlpatterns = [
    path('', index),
    path('customer',CustomerViewset.as_view({
        'get':'list',
        'post':'create'
    })),
    path('customer/<str:pk>',CustomerViewset.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('products',ProductViewset.as_view({
        'get':'list',
        # 'post':'create'
    })),
    path('products/<str:pk>',ProductViewset.as_view({
        'get':'retrieve',
        # 'put':'update',
        # 'delete':'destroy'
    })),
]
