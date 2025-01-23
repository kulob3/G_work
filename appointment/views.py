from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from appointment.forms import AppointmentForm
from appointment.models import Appointment
from django.shortcuts import get_object_or_404

from clients.models import Client


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment

    def get_queryset(self):
        return Appointment.objects.all()


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('appointment:appointment_list')

    def form_valid(self, form):
        user = self.request.user
        client = get_object_or_404(Client, email=user)  # Ищем по объекту User, а не строке email
        form.instance.client = client
        form.instance.price = form.cleaned_data['service']
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm

    def get_success_url(self):
        return reverse('appointment:appointment_view', args=[self.object.pk])


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment:appointment_list')
    extra_context = {
        'title': 'Delete appointment'
    }




