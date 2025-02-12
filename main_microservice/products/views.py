from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .tasks import process_create, process_update, process_delete

# Create your views here.
def index(request):
    return HttpResponse("hello this is the index page") 




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