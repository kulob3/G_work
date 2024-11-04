from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from message.forms import MessageForm
from message.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.all()


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.slug = slugify(new_message.topic)
            new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('message:message_view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.topic)
            new_blog.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message:message_list')
    extra_context = {
        'title': 'Delete Message'
    }