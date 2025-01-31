from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from clients.forms import ClientForm
from clients.models import Client
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            return Client.objects.all()  # Админы и менеджеры видят всех
        return Client.objects.filter(email=user)  # Клиент видит только себя

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.filter(email=self.request.user).first()
        return context



class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Client, pk=pk)

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:client_list')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
        })
        return initial

    def form_valid(self, form):
        # Проверяем, существует ли уже клиент для текущего пользователя
        if Client.objects.filter(email=self.request.user).exists():
            form.add_error(None, 'A client with this email already exists.')
            return self.form_invalid(form)

        # Создаем клиента, связывая его с текущим пользователем
        client = form.save(commit=False)
        client.email = self.request.user  # Привязываем клиента к текущему пользователю
        client.first_name = self.request.user.first_name
        client.last_name = self.request.user.last_name
        client.save()
        return redirect(self.success_url)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('clients:client_view', args=[self.object.pk])

    def form_valid(self, form):
        client = form.save(commit=False)
        client.first_name = form.cleaned_data['first_name']
        client.last_name = form.cleaned_data['last_name']
        client.save()
        return redirect(self.get_success_url())


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')
    extra_context = {
        'title': 'Delete Client'
    }


