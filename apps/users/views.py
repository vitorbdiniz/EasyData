from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# reset password
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from apps.users.services.generator import account_activation_token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail

from apps.users.forms import CreateUserForm, LoginForm, ForgotPassword, ResetPassword

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Conta criada para ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def forgot(request):
    form = ForgotPassword()
    if request.method == "POST":
        form = ForgotPassword(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data.get('email')
                print(email)
                uri = _generate_url_one_time_forgot_password('reset_password', request, email)
                print(uri)
                message = "Clique aqui para resetar sua senha: %s" % uri
                _send_mail_plain_text(message, email)
            except:
                messages.error(request, 'Esse email não está cadastrado em nossa base.')
                return redirect('forgot_password')
            messages.success(request, 'Email enviado com sucesso para ' + email)
            return redirect('login')

    context = {'form': form}
    return render(request, 'forgot_pass.html', context)


def _generate_url_one_time_forgot_password(reverse_view, request, email):
    user = User.objects.get(email=email)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = account_activation_token.make_token(user)
    link = reverse(reverse_view, kwargs={'uidb64': uid, 'token': token})
    current_site = get_current_site(request)
    default_domain = 'http://' + current_site.domain + link
    url = default_domain
    return url


def _send_mail_plain_text(message, dist):
    subject = 'Resetar senha'
    plain_message = message
    from_email = 'EasyData'
    to = dist
    mail.send_mail(subject, plain_message, from_email, [to])


def reset_password(request, uidb64, token):
    form = ResetPassword()
    if request.method == "POST":
        form = ResetPassword(request.POST)
        if form.is_valid():
            uid = urlsafe_base64_decode(uidb64)
            try:
                user = User.objects.get(pk=uid)
            except:
                messages.error(request, "Página inválida")
                return redirect('login')
            password1 = form.cleaned_data.get('password1')
            if not account_activation_token.check_token(user, token):
                messages.error(request, "Página inválida")
                return redirect('login')
            
            user.set_password(password1)
            user.save()
            messages.success(request, 'Senha alterada com sucesso')
            return redirect('login')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'reset_password.html', context)
