from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from blog.forms import BlogForm
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        self.object.views += 1
        self.object.save()
        return self.object

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_view', args=[self.kwargs.get('pk')])

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
