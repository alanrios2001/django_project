from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
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


@login_required(login_url="/login/")
def lists_view(request):
    if request.method == 'POST':
        # lida com a exclusão de listas
        if 'delete' in request.POST:
            lista_id = request.POST.get('delete')
            lista = get_object_or_404(Listas, id=lista_id, id_usuario=request.user)
            lista.deleted_at = datetime.now()
            lista.save()
            # itens = Itens.objects.filter(id_lista=lista.id, deleted_at=None)
            # for item in itens: # Apagando os itens da respectiva lista
            #     item.deleted_at = lista.deleted_at
            #     item.save()
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


@login_required(login_url='/login/')
def itens_view(request, list_name):
    form = ItensForm()
    try:
        lista = Listas.objects.get(nome=list_name, id_usuario=request.user)
    except Listas.DoesNotExist:
        raise Http404("Lista not found.")
    
    if request.method == 'POST':
        # lida com a exclusão de itens
        print("Loaded")
        if 'delete' in request.POST:
            item_id = request.POST.get('delete')
            item = get_object_or_404(Itens, id=item_id)
            item.deleted_at = datetime.now()
            item.save()
            # Include the list_name in the redirect
            return redirect('to_do_itens', list_name=item.id_lista.nome)

        # lida com a edição de itens
        elif 'edit' in request.POST:
            item_id = request.POST.get('edit')
            item = get_object_or_404(Itens, id=item_id)
            new_name = request.POST.get('new_name_' + item_id)
            if new_name:
                item.nome = new_name
                item.save()
            return redirect('to_do_itens', list_name=lista.nome)
        
        # lida com mudança de status do item
        elif 'toggle_status' in request.POST:
            item_id = request.POST.get('toggle_status')
            item = get_object_or_404(Itens, id=item_id)
            item.status = not item.status  # Toggle status
            print(item.status)
            item.save()
            return redirect('to_do_itens', list_name=lista.nome)

        # lida com a adição de itens
        elif "add_item" in request.POST:
            form = ItensForm(request.POST)
            if form.is_valid():
                lista = Listas.objects.get(nome=list_name, id_usuario=request.user)
                novo_item = form.save(commit=False)
                novo_item.id_lista = lista
                novo_item.save()
                # Include the list_name in the redirect
                return redirect('to_do_itens', list_name=lista.nome)

    else:
        form = ItensForm()# Re-assert form initialization for GET requests

    itens = Itens.objects.filter(id_lista=lista.id, deleted_at=None)
    return render(request, "to_do_list/list_itens.html", {'itens': itens, 'lista': lista,'form': form})


@login_required(login_url="/login/")
def lists_itens_view(request):
    return render(request, "to_do_list/list_itens.html")


