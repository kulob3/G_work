from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from service.forms import ServiceForm
from service.models import Service


class ServiceListView(ListView):
    model = Service

    def get_queryset(self):
        return Service.objects.all()


class ServiceDetailView(DetailView):
    model = Service


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('service:service_list')

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     if form.is_valid():
    #         new_service = form.save(commit=False)
    #         new_service.slug = slugify(new_.email)
    #         new_doctor.save()
    #     return super().form_valid(form)


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm

    def get_success_url(self):
        return reverse('service:service_view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_service = form.save()
            new_service.slug = slugify(new_service.name)
            new_service.save()
        return super().form_valid(form)


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('service:service_list')
    extra_context = {
        'title': 'Delete service'
    }