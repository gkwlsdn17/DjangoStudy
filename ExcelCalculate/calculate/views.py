from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def calculate(request):
    return HttpResponse("calculate, calculate function!")