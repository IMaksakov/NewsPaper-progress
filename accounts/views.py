from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Author
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from news.filters import PostFilter
from news.models import Post, Category

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors'):
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('news/')


class AccessView(View, PermissionRequiredMixin):
    permission_required = 'add_news'

########################################################
# class CategoryListView(ListView):
#     model = Post
#     template_name = 'templates/category_list.html'
#     context_object_name = 'category_news_list'
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Category, id = self.kwargs['pk'])
#         queryset = Post.objects.filter(category = self.category).order_by('-date')
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
#         context['category'] = self.category
#         return context
#
#
# @login_required
# def subscribe(request, pk):
#     user =request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#     message = 'Вы успешно подписались на рассылку новостей категории'
#
#     return render(request, 'templates/subscribe.html', {'category': category, 'message': message})
