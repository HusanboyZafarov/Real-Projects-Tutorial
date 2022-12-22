from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import UpdateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from works.models import Work
from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'full_name', 'bio', 'telegram', 'instagram', 'website']


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
      model = User
      fields = ['username', 'email']


class AccountLogin(LoginView):
    template_name = 'login.html'
    success_url = '/'


class AccountLogout(LogoutView):
    template_name = 'logout.html'


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})


def profile(request, username):
    user = User.objects.get(username=username)
    works = Work.objects.select_related('author').filter(author=user)
    context = {
        'user': user,
        'works': works
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/account/login/')
def settings(request):
    user = User.objects.get(id=request.user.id)
    works = Work.objects.select_related('author').filter(author=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print('ok')
            form.save()
            messages.add_message(request, messages.INFO, 'Profil muvaffaqiyatli tahrirlandi')
            return redirect('/account/settings/')
    else:
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
    return render(request, 'settings.html', {'works': works, 'form': form})


