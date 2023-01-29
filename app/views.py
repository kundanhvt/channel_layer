from django.shortcuts import render

# Create your views here.

def home(request, group_name):
    return render(request,'app/index.html',context={'group_name':group_name})