from django.shortcuts import render

def house_list(request):
    return render(request, 'houses/houses.html')