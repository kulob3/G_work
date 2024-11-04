from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from clients.forms import ClientForm
from clients.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        return Client.objects.all()


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.is_valid():
            new_client = form.save()
            new_client.slug = slugify(new_client.name)
            new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('client:client_view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')
    extra_context = {
        'title': 'Delete Client'
    }


