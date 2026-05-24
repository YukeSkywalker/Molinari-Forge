from django.shortcuts import render

def users_view(request):
    return render(request, "profile/profile.html")
def admin_panel_view(request):
    return render(request, "admin_panel/admin_panel.html")