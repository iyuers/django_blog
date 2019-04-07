from django.db import models
from django.contrib.auth.models import AbstractUser


# 自定义 Manager 用于归档中需求的对 data_publish 字段的截取
class ArticleManager(models.Manager):
    def distinct_date(self):
        data_list = []
        for data_time in self.values('data_publish'):
            # 这里可以是使用 html 文件中的归档格式，
            # 但是如果在其他地方也要用到，就需要定义的更加灵活
            # 需要用到 datetime.datetime 的 strftime 方法，用于格式化时间
            # 注意这个格式化里面，不能有中文！！
            data_time = data_time['data_publish'].strftime('%Y/%m')
            if data_time not in data_list:
                data_list.append(data_time)
        return data_list


# Create your models here.
# 用户
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


# 分类
class Category(models.Model):
    name = models.CharField(max_length=30, default='默认', verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='分类排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index']

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    data_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-data_publish']

    def __str__(self):
        return self.title


# 评论
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名', default="匿名用户")
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮件地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    data_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='用户')
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE, verbose_name='文章')
    pid = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-data_publish']

    def __str__(self):
        return str(self.id)


# 友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    data_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title


# 广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(verbose_name='回调url')
    data_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排序(从小到大)')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title





















