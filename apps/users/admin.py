from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'house', 'questionnaire_completed', 'is_staff')
    list_filter = ('role', 'house', 'questionnaire_completed', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Molinari Forge', {
            'fields': ('role', 'house', 'school_class', 'questionnaire_completed'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Molinari Forge', {
            'fields': ('role', 'first_name', 'last_name', 'email'),
        }),
    )

    # I docenti vengono registrati dall'admin: permetti impostare il ruolo
    def save_model(self, request, obj, form, change):
        if not change:
            # Nuovo utente creato dall'admin
            if not obj.email and obj.role in ('teacher', 'admin'):
                pass  # email opzionale per docenti
        super().save_model(request, obj, form, change)
