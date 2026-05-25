from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps


def teacher_required(view_func):
    """Solo docenti/admin possono accedere."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_teacher:
            return redirect('student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    """Solo studenti possono accedere."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_teacher:
            return redirect('teacher_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def questionnaire_required(view_func):
    """Richiede che lo studente abbia completato il questionario."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_teacher and not request.user.questionnaire_completed:
            return redirect('questionnaire')
        return view_func(request, *args, **kwargs)
    return wrapper
