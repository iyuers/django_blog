"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
path and re_path
    path('index/<int:number>', views, name="index")
    re_path('index/(?<number_id>\d+)', views, name="index")
"""
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    path('index', views.index, name="index"),
    path('archive', views.archive, name="archive"),
    path('article', views.article, name="article"),
    path('comment_post', views.comment_post, name="comment_post"),
    path('register', views.do_register, name="register"),
    path('login', views.do_login, name="login"),
    path('logout', views.do_logout, name="logout"),
]
