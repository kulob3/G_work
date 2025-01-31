from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from appointment.forms import AppointmentForm, AdminAppointmentForm
from appointment.models import Appointment
from django.shortcuts import get_object_or_404
from clients.models import Client
from django.shortcuts import redirect
from django.contrib import messages


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "appointment/appointment_list.html"
    context_object_name = "appointments"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            return Appointment.objects.all()  # Админы и менеджеры видят все записи

        # Проверяем, есть ли у пользователя объект Client
        client = Client.objects.filter(email=user).first()
        if client:
            return Appointment.objects.filter(client=client)  # Клиент видит только свои записи

        return Appointment.objects.none()  # Если клиент не найден, ничего не показываем

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.filter(email=self.request.user).first()
        return context


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    success_url = reverse_lazy('appointment:appointment_list')

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser or hasattr(user, 'is_manager') and user.is_manager:
            return AdminAppointmentForm
        return AppointmentForm

    def form_valid(self, form):
        user = self.request.user
        client = get_object_or_404(Client, email=user)  # Ищем по объекту User, а не строке email
        form.instance.client = client
        form.instance.price = form.cleaned_data['service']
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser or hasattr(user, 'is_manager') and user.is_manager:
            return AdminAppointmentForm
        return AppointmentForm

    def form_valid(self, form):
        if 'cancel_appointment' in self.request.POST:
            form.instance.status = 'Отменен'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('appointment:appointment_view', args=[self.object.pk])


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment:appointment_list')
    extra_context = {
        'title': 'Delete appointment'
    }

def cancel_appointment(request, pk):
    """Функция отмены приема"""
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'Отменен'
    appointment.save()
    messages.success(request, 'Appointment has been cancelled.')
    return redirect('appointment:appointment_view', pk=pk)


def confirm_appointment(request, pk):
    """Функция подтверждения приема менеджером"""
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'Подтвержден'
    appointment.save()
    messages.success(request, 'Appointment has been confirmed.')
    return redirect('appointment:appointment_view', pk=pk)



