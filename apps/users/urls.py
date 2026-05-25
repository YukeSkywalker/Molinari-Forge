from django.urls import path
from .views import (
    CustomLoginView,
    logout_view,
    register_view,
    questionnaire_view,
    dashboard_redirect,
    student_dashboard,
    teacher_dashboard,
    view_profile,
    home_redirect,
    admin_panel_view,
)

urlpatterns = [
    # Auth
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/register/', register_view, name='register'),
    path('auth/questionnaire/', questionnaire_view, name='questionnaire'),

    # Dashboard
    path('dashboard/', dashboard_redirect, name='dashboard'),
    path('dashboard/student/', student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', teacher_dashboard, name='teacher_dashboard'),

    # Admin panel
    path('admin-panel/', admin_panel_view, name='admin_panel'),

    # Profile
    path('profile/', view_profile, name='profile'),

    # Home
    path('', home_redirect, name='home'),
]
