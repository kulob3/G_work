from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from blog.models import Blog
from clients.models import Client
from sending.forms import SendingForm, SendingManagerForm
from sending.models import Sending, MailingStatus
from sending.services import send_mailing


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
        return JsonResponse({'status': 'success', 'message': 'Рассылки запущены'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@require_POST
def stop_all_mailings(request):
    """Остановка всех рассылок через страницу"""
    status = MailingStatus.objects.first()
    if status:
        status.is_running = False
        status.save()
    return JsonResponse({'status': 'success', 'message': 'Рассылки остановлены'})


def get_mailing_status(request):
    """Получение статуса рассылок для отображения на странице"""
    status = MailingStatus.objects.first()
    if status and status.is_running:
        return JsonResponse({'status': 'running', 'message': 'Рассылки запущены'})
    return JsonResponse({'status': 'stopped', 'message': 'Рассылки остановлены'})

class SendingListView(ListView):
    model = Sending


class SendingDetailView(DetailView):
    model = Sending


class SendingCreateView(CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy('sending:sending_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the owner to the current user
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)


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

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_articles': random_articles,
    }
    return render(request, 'sending/home.html', context)