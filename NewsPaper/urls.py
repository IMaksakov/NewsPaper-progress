from django.contrib import admin
from django.urls import path, include
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),

]
