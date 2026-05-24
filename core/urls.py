from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_panel/', include('apps.users.urls')),

    path("", include('apps.dashboard.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('houses/', include('apps.houses.urls')),
    path("leaderboard/", include("apps.leaderboard.urls")),
    path("requests_list/", include("apps.requests_app.urls")),
    path("rewards/", include("apps.rewards.urls")),
    path("notifications/", include("apps.notifications_app.urls")),
    path("profile/", include("apps.users.urls")),
]