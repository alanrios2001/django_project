from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from app_projeto.models import Listas, Itens
from .forms import ListasForm, ItensForm


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


@login_required(login_url="/accounts/login/")
def lists_view(request):
    listas = Listas.objects.filter(id_usuario=request.user, deleted_at=None)
    form = ListasForm()

    if request.method == 'POST':
        # lida com a exclusão de listas
        if 'delete' in request.POST:
            lista_id = request.POST.get('delete')
            lista = get_object_or_404(Listas, id=lista_id, id_usuario=request.user)
            lista.deleted_at = datetime.now()
            lista.save()
            return redirect('to_do_list')

        # lida com a adição de listas
        elif "add_list" in request.POST:
            form = ListasForm(request.POST)
            if form.is_valid():
                nova_lista = form.save(commit=False)
                nova_lista.id_usuario = request.user
                nova_lista.save()
                return redirect('to_do_list')

        # lida com a seleção de listas
        elif 'select' in request.POST:
            return redirect('list_detail', id_lista=request.POST.get('select'))

    return render(request, "to_do_list/lists.html", {'listas': listas, 'form': form})


@login_required(login_url="/accounts/login/")
def list_detail_view(request, id_lista):
    lista = get_object_or_404(Listas, id=id_lista, id_usuario=request.user)
    itens = Itens.objects.filter(id_lista=lista, deleted_at=None)
    form = ListasForm()

    if request.method == 'POST':
        # lida com a adição de itens
        if 'add_item' in request.POST:
            form = ItensForm(request.POST)
            if form.is_valid():
                novo_item = form.save(commit=False)
                novo_item.id_lista_id = id_lista
                novo_item.save()
                return redirect('list_detail', id_lista=id_lista)
        # lida com a remoção de itens
        elif 'delete' in request.POST:
            item_id = request.POST.get('delete')
            item = get_object_or_404(Itens, id=item_id)
            item.deleted_at = datetime.now()
            item.save()
            return redirect('list_detail', id_lista=id_lista)
        # lida com a marcação de itens feitos/não feitos
        elif 'is_done' in request.POST:
            item = get_object_or_404(Itens, id=request.POST.get('item_id'))
            item.is_done = request.POST.get('is_done')
            item.save()
            return HttpResponse(status=204)
        elif 'return' in request.POST:
            return redirect('to_do_list')

    return render(request, "to_do_list/list_detail.html", {'lista': lista, 'itens': itens, 'form': form})
