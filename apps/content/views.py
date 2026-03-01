from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm


class PostListView(ListView):
    """Список всех постов"""
    model = Post
    template_name = 'content/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    """Детальный просмотр поста"""
    model = Post
    template_name = 'content/post_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.can_view(request.user):
            if not request.user.is_authenticated:
                return redirect(f"{reverse_lazy('accounts:login')}?next={request.path}")
            else:
                # ВРЕМЕННО: вместо редиректа на payments показываем сообщение
                # Позже здесь будет редирект на payments:subscription
                from django.http import HttpResponse
                return HttpResponse(
                    "Для просмотра платного контента нужна подписка. Скоро здесь будет страница оплаты!")

        return super().get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание нового поста"""
    model = Post
    form_class = PostForm
    template_name = 'content/post_form.html'
    success_url = reverse_lazy('content:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование поста"""
    model = Post
    form_class = PostForm
    template_name = 'content/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('content:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление поста"""
    model = Post
    success_url = reverse_lazy('content:post_list')
    template_name = 'content/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
