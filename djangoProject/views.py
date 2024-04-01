from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirecione para uma página de sucesso.
            return redirect('pagina_de_sucesso')
        else:
            # Retorne um erro de 'login inválido'.
            return render(request, 'login.html', {'error': 'Login inválido.'})
    else:
        return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)  # Loga o usuário automaticamente após o cadastro
            return redirect('pagina_de_sucesso')  # Redireciona para a página desejada
        except:
            return render(request, 'signup.html', {'error': 'Erro ao criar usuário. Talvez o nome de usuário já exista.'})
    else:
        return render(request, 'signup.html')


def success_view(request):
    # A decoração @login_required irá redirecionar usuários não autenticados para a página de login
    return render(request, 'success.html')
