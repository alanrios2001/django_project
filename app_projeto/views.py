from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from app_projeto.models import Listas, Itens
from .forms import ListasForm


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
            return redirect("to_do_list")
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
            return redirect("to_do_list")
        else:
            return render(
                request,
                "auth/signup.html",
                {"error": "Erro ao criar usuário. Talvez o nome de usuário já exista."},
            )

    else:
        return render(request, "auth/signup.html")


@login_required(login_url="/login/")
def lists_view(request):
    if request.method == 'POST':
        # lida com a exclusão de listas
        if 'delete' in request.POST:
            lista_id = request.POST.get('delete')
            lista = get_object_or_404(Listas, id=lista_id, id_usuario=request.user)
            lista.deleted_at = datetime.now()
            lista.save()
            return redirect('to_do_list')
        # lida com a edição de listas
        elif 'edit' in request.POST:
            pass
        # lida com a adição de listas
        elif "add_list" in request.POST:
            form = ListasForm(request.POST)
            if form.is_valid():
                nova_lista = form.save(commit=False)
                nova_lista.id_usuario = request.user
                nova_lista.save()
                return redirect('to_do_list')
    else:
        form = ListasForm()

    listas = Listas.objects.filter(id_usuario=request.user, deleted_at=None)
    return render(request, "to_do_list/lists.html", {'listas': listas, 'form': form})


@login_required(login_url="/login/")
def lists_itens_view(request):
    return render(request, "to_do_list/list_itens.html")
