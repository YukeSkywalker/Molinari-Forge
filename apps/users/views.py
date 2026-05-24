from django.shortcuts import render

def users_view(request):
    return render(request, "profile/profile.html")

def admin_panel_view(request):
    return render(request, "admin/admin_panel.html")