from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from blog.models import Blog
from clients.models import Client
from doctors.models import Doctor
from sending.forms import SendingForm, SendingManagerForm
from sending.models import Sending, MailingStatus
from sending.services import send_mailing
from service.models import Service
from django.shortcuts import render
from .forms import FeedbackForm
from django.core.mail import send_mail


@csrf_exempt
@require_POST
def start_all_mailings(request):
    """Запуск всех рассылок через страницу"""
    try:
        status = MailingStatus.objects.first()
        if status:
            status.is_running = True
            status.save()
        else:
            MailingStatus.objects.create(is_running=True)
        send_mailing()
        return JsonResponse({'status': 'success', 'service': 'Рассылки запущены'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'service': str(e)})

@csrf_exempt
@require_POST
def stop_all_mailings(request):
    """Остановка всех рассылок через страницу"""
    status = MailingStatus.objects.first()
    if status:
        status.is_running = False
        status.save()
    return JsonResponse({'status': 'success', 'service': 'Рассылки остановлены'})


def get_mailing_status(request):
    """Получение статуса рассылок для отображения на странице"""
    status = MailingStatus.objects.first()
    if status and status.is_running:
        return JsonResponse({'status': 'running', 'service': 'Рассылки запущены'})
    return JsonResponse({'status': 'stopped', 'service': 'Рассылки остановлены'})

class SendingListView(LoginRequiredMixin, ListView):
    model = Sending


class SendingDetailView(LoginRequiredMixin, DetailView):
    model = Sending


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy('sending:sending_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the owner to the current user
        if form.is_valid():
            new_sending = form.save(commit=False)
            new_sending.slug = slugify(new_sending.name)
            new_sending.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        return form




class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingForm

    def get_success_url(self):
        return reverse('sending:sending_view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return SendingForm
        if user.groups.filter(name='manager').exists():
            return SendingManagerForm
        raise PermissionDenied

class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy('sending:sending_list')
    extra_context = {
        'title': 'Delete Sending'
    }

def home(request):
    """Получение общей информации для главной страницы"""
    total_mailings = Sending.objects.count()
    active_mailings = Sending.objects.filter(status='active').count()
    unique_clients = Client.objects.distinct().count()
    random_articles = Blog.objects.order_by('?')[:3]
    total_doctors = Doctor.objects.count()
    total_services = Service.objects.count()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                f'Feedback from {name}',
                message,
                '9272060714@mail.ru',  # Ensure this matches EMAIL_HOST_USER
                ['kulob3@yandex.ru'],
                fail_silently=False,
            )
            return redirect('home')
    else:
        form = FeedbackForm()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_articles': random_articles,
        'total_doctors': total_doctors,
        'total_services': total_services,
        'form': form,
    }
    return render(request, 'sending/home.html', context)



def contacts(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                f'Feedback from {name}',
                message,
                '9272060714@mail.ru',  # Ensure this matches EMAIL_HOST_USER
                ['kulob3@yandex.ru'],
                fail_silently=False,
            )
            return redirect('contacts')
    else:
        form = FeedbackForm()

    context = {
        'form': form,
    }
    return render(request, 'sending/contacts.html', context)