from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from message.models import Message


class MessageListView(ListView):
    model = Message
    # template_name = 'message/message_list.html'
    # context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.all()

class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = "__all__"
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.topic)
            new_blog.save()
        return super().form_valid(form)

class MessageUpdateView(UpdateView):
    model = Message
    fields = '__all__'

    def get_success_url(self):
        return reverse('message:message_view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.topic)
            new_blog.save()
        return super().form_valid(form)

class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('message:message_list')
    extra_context = {
        'title': 'Delete Message'
    }