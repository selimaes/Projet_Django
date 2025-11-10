from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import logout

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # ou vers une autre page si tu veux
    else:
        form = UserRegisterForm()

    return render(request, "user/register.html", {"form": form})
def logout_view(req):
    logout(req)
    return redirect("login")
    