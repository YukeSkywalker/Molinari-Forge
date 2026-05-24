from django.shortcuts import render

def request_view(request):
    return render(request, "requests/request.html")