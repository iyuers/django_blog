from django.shortcuts import render, redirect
import logging
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import cache_page
from django.db.models import Count
from blog.forms import CommentForm, UserForm
from blog.models import *

logger = logging.getLogger('blog_views')


# 设置上下文，适用于很少有变动的数据

def get_local_msg(request):
    # 网站信息
    SITE_NAME = settings.SITE_NAME
    SITE_DESC= settings.SITE_DESC
    WEIBO_SINA = settings.WEIBO_SINA
    WEIBO_TENCENT = settings.WEIBO_TENCENT
    PRO_RSS = settings.PRO_RSS
    PRO_EMAIL = settings.PRO_EMAIL

    # 导航全局变量
    category_list = Category.objects.all()
    # 归档全局变量
    date_list = Article.objects.distinct_date()
    # 广告信息，添加到上下文
    ad_list = Ad.objects.all()
    # 浏览排行
    # 评论排行
    comment_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(id=comment['article']) for comment in comment_list]
    # 站长推荐
    # 标签云
    tag_list = Tag.objects.all()
    # 友情链接
    link_list = Links.objects.all()

    return locals()


# 抽象化 分页器，适用全局
def pagination(request, model_list, releases=10):
    paginator = Paginator(model_list, releases)
    # 验证用户输入
    try:
        page = int(request.GET.get('page', 1))
        # 获取分页后的 内容
        model_items = paginator.page(page)
    except (InvalidPage, EmptyPage, PageNotAnInteger) as e:
        logger.error(e)
        # 若用户输入不符合，则默认返回第一页
        model_items = paginator.page(1)

    page_list = list(range(1, paginator.num_pages + 1))

    return model_items, page_list


# Create your views here.
@cache_page(60, key_prefix='index')
def index(request):
    try:
        # 分类信息获取(导航数据)
        # 确保通用性，将其添加到上下文
        # category_list = Category.objects.all()
        # 广告数据(幻灯片)
        # 很少变化的，确保通用性，添加到上下文
        # ad_list = Ad.objects.all()

        # 文章获取(正文)
        article_list = Article.objects.all()
        # # 抽象化分页器,
        # paginator = Paginator(article_list, 10)
        # # 验证用户输入
        # try:
        #     page = int(request.GET.get('page', 1))
        #     # 获取分页后的 内容
        #     article_items = paginator.page(page)
        # except (InvalidPage, EmptyPage, PageNotAnInteger) as e:
        #     # 若用户输入不符合，则默认返回第一页
        #     article_items = paginator.page(1)

        # 文章归档
        # 先要去获取文章的 年份-月份
        # 确保通用性，可以将其添加到上下文
        # date_list = Article.objects.distinct_date()

        # 抽象化分页器
        # page_list = list(range(1, paginator.num_pages + 1))

        # 调用抽象化的分页器，既可获得分页的文章内容和分页数目列表
        # 后期调用分页抽象函数，必须将返回的内容数据命名为 page_items
        # 有利于在 html 页面统一调用分页器，实现代码重用
        page_items, page_list = pagination(request, article_list)

    except Exception as e:
        logger.error(e)

    return render(request, 'index.html', locals())


def archive(request):
    try:
        year = request.GET.get('year')
        month = request.GET.get('month')
        article_list = Article.objects.filter(data_publish__icontains=year + '-' + month)

        page_items, page_list = pagination(request, article_list, releases=3)
    except Exception as e:
        logger.error(e)

    return render(request, 'archive.html', locals())


# 实现文章详情页面
def article(request):
    try:
        # 获取文章的查询条件 id
        article_id = request.GET.get('id')
        try:
            # 通过条件查询数据库
            get_article = Article.objects.get(id=article_id)
        except Article.DoesNotExist as e:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论，如果是已登录用户，可以将 评论的用户名，邮箱等填写
        comment_form = CommentForm({
            'username': request.user.username,
            'email': request.user.email,
            'url': request.user.url,
            'id': article_id
        } if request.user.is_authenticated else {'article': article_id})

        # 获取评论信息
        comments = Comment.objects.filter(article=get_article).order_by('id')
        comment_list = []
        # 设定输出评论的级数，只有两级
        # 即 一篇文章的评论，有子评论，但是这个子评论是没有子评论
        for comment in comments:
            for item in comment_list:
                # 给 评论对象添加一个 childer_comment 属性
                # 用于在网页上方便输出评论的子评论
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                # 注意关系 comment.pid 表示 这个 comment 对象是有父级评论的
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            else:
                comment_list.append(comment)

    except Exception as e:
        print(e)
        logger.error(e)

    return render(request, 'article.html', locals())


# 提交表单 post
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        article_id = request.POST.get('article_id')
        username = request.POST.get('user')
        if comment_form.is_valid():
            comment = Comment.objects.create(
                username=comment_form.cleaned_data['username'],
                email=comment_form.cleaned_data['email'],
                url=comment_form.cleaned_data['url'],
                content=comment_form.cleaned_data['content'],
                article=Article.objects.get(id=article_id),
                user=User.objects.get(username=username) if request.user.is_authenticated else None,
            )
            # 可能的问题，html 中 form 提交的信息并不齐全
            # 缺少 article 和 user
            comment.save()
        else:
            return render(request, 'failure.html')
    except Exception as e:
        logger.error(e)

    # 跳转到当前网页的 原生 url，包含 GET 提交的数据
    # 例如：localhost:8000/blog/article?id=2&....
    return redirect(request.META['HTTP_REFERER'])


# 用户功能 注册、登录和注销
def do_register(request):
    try:
        if request.method == 'POST':
            userform = UserForm(request.POST, request.FILES)
            if userform.is_valid():
                user = User.objects.create(
                    username=userform.cleaned_data['username'],
                    password=make_password(userform.cleaned_data['password']),
                    email=userform.cleaned_data['email'],
                    url=userform.cleaned_data['url'],
                    avatar=request.FILES.get('avatar'),
                )
                user.save()

                # 进行登录操作和验证
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                print('source_url', request.POST.get('source'))
                return redirect(request.POST.get('source'))
            else:
                return render(request, 'failure.html', {'reason': userform.errors})
        else:
            userform = UserForm()

    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


# 登录
def do_login(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            print('username', username)
            print(password)

            # 验证用户名和密码是否有效
            user = authenticate(username=username, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect(request.POST.get('source'))
            else:
                return render(request, 'failure.html', {'reason': '登录失败！'})
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])
