from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from doctors.forms import DoctorForm
from doctors.models import Doctor


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctors/doctor_list.html'

    def get_queryset(self):
        return Doctor.objects.all()


class DoctorDetailView(DetailView):
    model = Doctor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['can_edit'] = user.is_authenticated and (
                    user.is_superuser or user.has_perm('app_name.manager_permission'))
        return context


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    success_url = reverse_lazy('doctors:doctor_list')


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm

    def get_success_url(self):
        return reverse('doctors:doctor_view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_doctor = form.save()
            new_doctor.slug = slugify(new_doctor.email)
            new_doctor.save()
        return super().form_valid(form)


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('doctors:doctor_list')
    extra_context = {
        'title': 'Delete service'
    }

