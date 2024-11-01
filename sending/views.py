from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from config.settings import MANAGER_PERMISSIONS
from sending.forms import SendingForm, SendingManagerForm
from sending.models import Sending
from sending.services import send_mailing


@csrf_exempt
@require_POST
def start_all_mailings(request):
    try:
        send_mailing()
        return JsonResponse({'status': 'success', 'message': 'Рассылки запущены'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def stop_all_mailings(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Рассылки остановлены'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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
