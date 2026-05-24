from django.shortcuts import render


def student_dashboard(request):
    return render(request, "dashboard/student_dashboard.html")