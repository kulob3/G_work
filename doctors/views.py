from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from doctors.forms import DoctorForm
from doctors.models import Doctor
from django.shortcuts import render


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor

    def get_queryset(self):
        return Doctor.objects.all()


class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    # success_url = reverse_lazy('doctors:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.is_valid():
            new_doctor = form.save(commit=False)
            new_doctor.slug = slugify(new_doctor.topic)
            new_doctor.save()
        return super().form_valid(form)


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm

    # # def get_success_url(self):
    #     return reverse('doctors:message_view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_doctor = form.save()
            new_doctor.slug = slugify(new_doctor.topic)
            new_doctor.save()
        return super().form_valid(form)


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    # success_url = reverse_lazy('doctors:message_list')
    extra_context = {
        'title': 'Delete doctors'
    }

