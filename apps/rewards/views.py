from django.shortcuts import render

def rewards_view(request):
    return render(request, "rewards/rewards.html")