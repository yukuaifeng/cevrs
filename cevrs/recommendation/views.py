from django.http import HttpResponse
from .models import GradeAll, ControlLine, StudentNumber, User
from rest_framework import viewsets
from .serializers import GradeAllSerializer, ControlLineSerializer, StudentNumberSerializer, UserSerializer


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Success get in views")
    # if(request.method == 'POST'):
    #     print("yes")
    #     return HttpResponse("Hello, world. Success get in views")
