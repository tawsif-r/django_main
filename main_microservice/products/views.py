from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .tasks import process_create, process_update, process_delete

from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Products, Customer
from .serializers import CustomerSerializer,ProductSerializer
from .publish import *

# Create your views here.
class ProductViewset(viewsets.ViewSet):
    def list(self, request): # api/products
        products = Products.objects.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)
    


    def create(self, request): # api/products
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        product_instance = serializer.save()
        product_data = {
            'id': product_instance.id,
            'title': product_instance.title,
            'image': product_instance.image 
        }
        # publish_message("products_exchange","products.create",product_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED) 
    



    def retrieve(self, request, pk = None): # api/products/<str:id>
        product = Products.objects.get(id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)




    def update(self, request, pk = None): # api/products/<str:id>
        product = Products.objects.get(id=pk)
        serializer = ProductSerializer(instance = product, data = request.data)
        serializer.is_valid(raise_exception=True)
        product_instance = serializer.save()
        product_data ={
            'id' : product_instance.id,
            'title' : product_instance.title,
            'image' : product_instance.image
        }
        # publish_message("products_exchange","products.update",product_data)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    



    def destroy(self, request, pk = None): 
        product = Products.objects.get(id = pk)
        product.delete()
        data = {
            'id' : pk
        }
        # publish_message("products_exchange","products.delete",data)
        return Response(status= status.HTTP_204_NO_CONTENT)
    
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




