from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostEdit, PostDelete, PostSearch, ArticleCreate
from news.views import CategoryListView
from .models import Category
from .views import subscribe


#from news.views import NewsList, NewsDetails, NewsSearch, NewsCreateNew, NewsUpdateView, upgrade_me, CategoryListView

urlpatterns = [
    path('', PostsList.as_view(), name='news_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostEdit.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]
