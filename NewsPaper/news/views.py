from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import models
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import get_object_or_404
from django.core.cache import cache


class NewsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-date'
    template_name = '../templates/flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class CategoryListView(NewsList):
    model = Post
    template_name = '../templates/flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на категорию'
    return render(request, '../templates/flatpages/subscribe.html', {'category': category, 'message': message})


class SearchList(ListView):
    model = Post
    ordering = '-date'
    template_name = '../templates/flatpages/search.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = '../templates/flatpages/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', 0)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj

class ADD(PermissionRequiredMixin, CreateView):
    template_name = '../templates/flatpages/add.html'
    form_class = PostForm
    permission_required = ('news.add_post')


class Update(PermissionRequiredMixin, UpdateView):
    template_name = '../templates/flatpages/add.html'
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class Delete(PermissionRequiredMixin, DeleteView):
    template_name = '../templates/flatpages/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post')