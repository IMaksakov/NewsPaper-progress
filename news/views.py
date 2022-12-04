from xml.dom import ValidationErr

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from news.models import Post, Category
from news.filters import PostFilter
from django.views.generic.edit import CreateView





class PostsList(ListView):
    model = Post
    ordering = '-posting_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3


    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = "Новые статьи в пятницу"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        con = super().get_context_data(**kwargs)
        con['filterset'] = self.filterset
        return con


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    permission_required = ('newspage.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/create/':
                post.type_post = 'news'
            elif path_info == '/articles/create/':
                post.type_post = 'articles'
        post.save()
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newspage.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            pub_path = self.request.META['PATH_INFO']
            pub_type = pub_path.split('/')[1]
            if pub_type == 'articles' and self.object.type_post == 'articles' or pub_type == 'news' and self.object.type_post == 'news':
                return super().form_valid(form)
            else:
                raise ValidationErr(
                    f'Редактирование невозможно: {pub_path} не является публикацией {self.object.type_post}')


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

class PostSearch(ListView):
    model = Post
    ordering = '-posting_time'
    template_name = 'post_search.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class ArticleCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    permission_required = 'add_news'
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_field = 'article'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)



class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id = self.kwargs['pk'])
        queryset = Post.objects.filter(category = self.category).order_by('-posting_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user =request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

