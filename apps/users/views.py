from django.shortcuts import render

def users_view(request):
    return render(request, "profile/profile.html")