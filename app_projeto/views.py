from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def home_view(request):
    return render(request, "home/home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirecione para uma página de sucesso.
            return redirect("pagina_de_sucesso")
        else:
            # Retorne um erro de 'login inválido'.
            return render(request, "auth/login.html", {"error": "Login inválido."})
    else:
        return render(request, "auth/login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        if created:
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("pagina_de_sucesso")
        else:
            return render(
                request,
                "auth/signup.html",
                {"error": "Erro ao criar usuário. Talvez o nome de usuário já exista."},
            )

    else:
        return render(request, "auth/signup.html")


def success_view(request):
    # A decoração @login_required irá redirecionar usuários não autenticados para a página de login
    return render(request, "to_do_list/success.html")
