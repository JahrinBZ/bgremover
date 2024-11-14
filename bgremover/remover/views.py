from django.shortcuts import render

# Create your views here.
def home(request):
    Name="Oindrilla"
    data={'name':Name}
    return render(request,"Hello.html",data)