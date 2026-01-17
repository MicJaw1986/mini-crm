from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, UserUpdateForm


class CustomLoginView(LoginView):
    """Widok logowania"""
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, f'Witaj ponownie, {form.get_user().first_name or form.get_user().username}!')
        return super().form_valid(form)


def register_view(request):
    """Widok rejestracji użytkownika"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Witaj, {user.first_name}! Twoje konto zostało utworzone.')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """Widok profilu użytkownika"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Twój profil został zaktualizowany.')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def logout_view(request):
    """Widok wylogowania"""
    logout(request)
    messages.info(request, 'Zostałeś wylogowany.')
    return redirect('accounts:login')
