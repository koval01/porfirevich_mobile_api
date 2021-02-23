from django.http import HttpResponse
from .api_worker import api_get_data

def load_data(request):
    data = api_get_data()
    return HttpResponse(data)
