from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import home_redirect

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Root → redirect intelligente
    path('', home_redirect, name='home'),

    # Tutte le URL auth + dashboard (users app)
    path('', include('apps.users.urls')),

    # Altre app
    path('houses/', include('apps.houses.urls')),
    path('leaderboard/', include('apps.leaderboard.urls')),
    path('requests/', include('apps.requests_app.urls')),
    path('rewards/', include('apps.rewards.urls')),
    path('notifications/', include('apps.notifications_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
