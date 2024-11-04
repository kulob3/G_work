import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, ListView
from django.utils.encoding import force_bytes
from config import settings
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, PasswordResetRequestForm
from users.models import User
from django.contrib.auth.tokens import default_token_generator
import string
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        print(url)
        send_mail(
            subject='Email confirmation',
            message=f'Click on the link to confirm your email: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def generate_random_password(length=12):
    """Функция для генерации случайного пароля"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))


def password_reset_request(request):
    """Функция для сброса пароля"""
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    new_password = generate_random_password()
                    user.set_password(new_password)
                    user.save()

                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        'new_password': new_password,
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            return redirect("users:password_reset_done")
    form = PasswordResetRequestForm()
    return render(request, "users/password_reset.html", {"form": form})


class UserListView(LoginRequiredMixin, ListView):
    model = User

class CustomLoginView(LoginView):
    """Класс для авторизации пользователя, не позволяет забаненным пользователям авторизоваться"""
    def form_valid(self, form):
        user = form.get_user()
        if user.banned:
            messages.error(self.request, 'Вы забанены.')
            return self.form_invalid(form)
        return super().form_valid(form)


@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='manager').exists())
def ban_user(request, user_id):
    """Проверка полномочий перед баном"""
    user_to_ban = get_object_or_404(User, pk=user_id)

    if request.user.is_superuser:
        if user_to_ban.is_superuser:
            messages.error(request, 'Администратор не имеет права банить администраторов.')
            return redirect('users:user_list')
    elif request.user.groups.filter(name='manager').exists():
        if user_to_ban.is_superuser or user_to_ban.groups.filter(name='manager').exists():
            messages.error(request, 'Менеджер не имеет права банить администраторов или менеджеров.')
            return redirect('users:user_list')

    user_to_ban.banned = True
    user_to_ban.save()
    messages.success(request, f'Пользователь {user_to_ban.email} забанен.')
    return redirect('users:user_list')

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='manager').exists())
def unban_user(request, user_id):
    """Проверка полномочий перед разбаном"""
    user_to_unban = get_object_or_404(User, pk=user_id)

    if request.user.is_superuser:
        if user_to_unban.is_superuser:
            return redirect('users:user_list')
    elif request.user.groups.filter(name='manager').exists():
        if user_to_unban.is_superuser or user_to_unban.groups.filter(name='manager').exists():
            return redirect('users:user_list')

    user_to_unban.banned = False
    user_to_unban.save()
    messages.success(request, f'Пользователь {user_to_unban.email} разбанен.')
    return redirect('users:user_list')
