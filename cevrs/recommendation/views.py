from django.http import HttpResponse


# Create your views here.
def index(request):
    if(request.method == 'POST'):
        print("yes")
        return HttpResponse("Hello, world. Success get in views")
