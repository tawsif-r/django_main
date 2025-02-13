from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .tasks import process_create, process_update, process_delete

from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Products, Customer
from .serializers import CustomerSerializer
from .publish import *


# Create your views here.
class CustomerViewset(viewsets.ViewSet):
    def list(self, request): # api/products
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers,many = True)
        return Response(serializer.data)
    


    def create(self, request): # api/Customer
        serializer = CustomerSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        customer_instance = serializer.save()
        customer_data = {
            'id': customer_instance.id,
            'name': customer_instance.name,
            'age': customer_instance.age 
        }
        publish_message("customer_exchange","customer.create",customer_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED) 
    



    def retrieve(self, request, pk = None): # api/Customer/<str:id>
        customer = Customer.objects.get(id = pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)




    def update(self, request, pk = None): # api/Customer/<str:id>
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(instance = customer, data = request.data)
        serializer.is_valid(raise_exception=True)
        customer_instance = serializer.save()
        customer_data ={
            'id' : customer_instance.id,
            'name' : customer_instance.name,
            'age' : customer_instance.age
        }
        publish_message("customer_exchange","customer.update",customer_data)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    



    def destroy(self, request, pk = None): 
        customer = Customer.objects.get(id = pk)
        customer.delete()
        data = {
            'id' : pk
        }
        publish_message("customer_exchange","customer.delete",data)
        return Response(status= status.HTTP_204_NO_CONTENT)
    
# Create your views here.
def index(request):
    return HttpResponse("hello this is the index page") 




"""Task assign for consumer"""

def create_product(request):
    if request.method == 'POST':
        data = {
            'id': request.POST.get('id'),
            'title': request.POST.get('title'),
            'image': request.POST.get('image')
        }
        process_create.delay(data)  # Call the Celery task asynchronously
        return JsonResponse({'status': 'Product creation task queued'})

def update_product(request):
    if request.method == 'POST':
        data = {
            'id': request.POST.get('id'),
            'title': request.POST.get('title'),
            'image': request.POST.get('image')
        }
        process_update.delay(data)  # Call the Celery task asynchronously
        return JsonResponse({'status': 'Product update task queued'})

def delete_product(request):
    if request.method == 'POST':
        data = {'id': request.POST.get('id')}
        process_delete.delay(data)  # Call the Celery task asynchronously
        return JsonResponse({'status': 'Product deletion task queued'})