from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import StudentRegisterForm, ForgeLoginForm
from .decorators import teacher_required, student_required


# =========================
# HOME REDIRECT
# =========================
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


# =========================
# LOGIN
# =========================
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = ForgeLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/dashboard/'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # Sessione scade alla chiusura del browser
            self.request.session.set_expiry(0)
        else:
            # Sessione dura 2 settimane
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# REGISTRAZIONE STUDENTE
# =========================
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = StudentRegisterForm()

    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Benvenuto, {user.first_name}! Completa il questionario per scoprire la tua casata.')
            return redirect('questionnaire')

    return render(request, 'auth/register.html', {'form': form})


# =========================
# QUESTIONARIO (solo studenti)
# =========================
@login_required
def questionnaire_view(request):
    user = request.user

    # Se ha già completato, vai alla dashboard
    if user.questionnaire_completed:
        return redirect('dashboard')

    # I docenti non fanno il questionario
    if user.is_teacher:
        return redirect('dashboard')

    if request.method == 'POST':
        # Assegna una casata in base alle risposte (logica semplice, da espandere)
        _assign_house(user, request.POST)
        user.questionnaire_completed = True
        user.save()
        messages.success(request, f'Sei stato assegnato alla casata {user.house.name}!' if user.house else 'Benvenuto nella Forge!')
        return redirect('student_dashboard')

    return render(request, 'auth/questionnaire.html')


def _assign_house(user, post_data):
    """Assegna una casata all'utente in base alle risposte del questionario."""
    from apps.houses.models import House
    houses = list(House.objects.all())
    if not houses:
        return

    # Logica di assegnazione: conta risposte e mappa alle case
    scores = {h.id: 0 for h in houses}
    house_map = {h.name.lower(): h for h in houses}

    answer = post_data.get('thinking_style', '')
    if answer == 'logic':
        h = house_map.get('algoritmia') or houses[0]
        scores[h.id] += 3
    elif answer == 'creative':
        h = house_map.get('byteon') or houses[min(1, len(houses)-1)]
        scores[h.id] += 3
    elif answer == 'security':
        h = house_map.get('cryptoria') or houses[min(2, len(houses)-1)]
        scores[h.id] += 3
    elif answer == 'network':
        h = house_map.get('netstorm') or houses[min(3, len(houses)-1)]
        scores[h.id] += 3

    answer2 = post_data.get('challenge', '')
    if answer2 == 'algorithms':
        h = house_map.get('algoritmia') or houses[0]
        scores[h.id] += 2
    elif answer2 == 'building':
        h = house_map.get('byteon') or houses[min(1, len(houses)-1)]
        scores[h.id] += 2
    elif answer2 == 'hacking':
        h = house_map.get('cryptoria') or houses[min(2, len(houses)-1)]
        scores[h.id] += 2
    elif answer2 == 'networks':
        h = house_map.get('netstorm') or houses[min(3, len(houses)-1)]
        scores[h.id] += 2

    # Assegna la casa con punteggio più alto
    best_id = max(scores, key=scores.get)
    user.house = next((h for h in houses if h.id == best_id), houses[0])
    user.save()


# =========================
# DASHBOARD REDIRECT (centrale)
# =========================
@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_teacher:
        return redirect('teacher_dashboard')

    # Studenti/teamleader che non hanno completato il questionario
    if not user.questionnaire_completed:
        return redirect('questionnaire')

    return redirect('student_dashboard')


# =========================
# DASHBOARD STUDENTE
# =========================
@login_required
@student_required
def student_dashboard(request):
    from apps.houses.models import House
    context = {
        'houses': House.objects.order_by('-total_points'),
    }
    return render(request, 'dashboard/student_dashboard.html', context)


# =========================
# DASHBOARD DOCENTE / ADMIN
# =========================
@login_required
@teacher_required
def teacher_dashboard(request):
    from apps.users.models import CustomUser
    context = {
        'total_students': CustomUser.objects.filter(role='student').count(),
        'pending_requests_count': 0,
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)


# =========================
# PROFILE
# =========================
@login_required
def view_profile(request):
    return render(request, 'profile/profile.html')


# =========================
# ADMIN PANEL
# =========================
@login_required
@teacher_required
def admin_panel_view(request):
    from apps.users.models import CustomUser
    from apps.houses.models import House
    context = {
        'students': CustomUser.objects.filter(role='student').select_related('house', 'school_class'),
        'houses': House.objects.all(),
    }
    return render(request, 'admin/admin_panel.html', context)
