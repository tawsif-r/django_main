from django.urls import path
from .views import index, CustomerViewset

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
    }))
]
