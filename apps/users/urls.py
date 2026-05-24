from django.urls import path
from . import views

urlpatterns = [
    path("", views.users_view, name="profile"),
    path("admin_panel/", views.admin_panel_view, name="admin_panel"),
]