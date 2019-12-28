# -*- coding: utf-8 -*-
# Create your views here.

import json,os
import yaml,pickle,base64
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from blog.models import Article, Category, Comment
from django.contrib.auth.models import User

def Index(request):
    """
    博客首页
    :param request:
    :return:
    """
    article_list = Article.objects.all().order_by('-date_time')[0:5]
    return render(request, 'blog/index.html', {"article_list": article_list,
                                               "source_id": "index"})


def Articles(request, pk):
    """
    博客列表页面
    :param request:
    :param pk:
    :return:
    """
    pk = int(pk)
    if pk:
        category_object = get_object_or_404(Category, pk=pk)
        category = category_object.name
        article_list = Article.objects.filter(category_id=pk)
    else:
        # pk为0时表示全部
        article_list = Article.objects.all()  # 获取全部文章
        category = u''
    return render(request, 'blog/articles.html', {"article_list": article_list,
                                                  "category": category,
                                                  })

def GetArticle(request, pk):
    pk = int(pk)    
    if pk:
        article = Article.objects.filter(pk=pk)[0]
        article_str = {}
        article_str = "title:'" + str(article.title) + "'\r\n"
        article_str += "date_time:'" + str(article.date_time) + "'\r\n"
        article_str += "content:'" + str(article.content) + "'\r\n"
        article_dict = {}
        article_dict["title"] = str(article.title)
        article_dict["date_time"] = str(article.date_time)
        article_dict["content"] = str(article.content)
        return HttpResponse(json.dumps(article_dict),content_type="application/json")
    else:
        # pk为0时表示全部
        article_list = Article.objects.all()  # 获取全部文章
        category = u''
        return render(request, 'blog/articles_error.html', {})
    pass

def UploadArticle(request):
    if request.method == "GET":
        return render(request, 'blog/upload.html', {})
    elif request.method == "POST":
        try:
            obj = request.FILES.get('fafafa')
            import os
            # 上传文件的文件名 
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            f = open(os.path.join(BASE_DIR, 'static', 'upload', obj.name), 'wb')
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
            article = yaml.load(file(os.path.join(BASE_DIR, 'static', 'upload', obj.name)))
            print article

            article = Article(title=article["title"], content=article["content"], date_time=article["date_time"],category=Category(id=1),author=User(id=1))
            article.save()
            return HttpResponse("上传成功！")
        except Exception as e:
            print e
            return HttpResponse("上传失败！")

def DownloadArticle(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        # path = 'blog/static/upload/../../../../flag'
        path = os.path.join(BASE_DIR, 'static', "./upload/%s" % request.GET['path'])
        with open(path, "rb") as f:
            content = f.read()
        return HttpResponse(content)
    except:
        return HttpResponse("Sorry, the file you were looking for was not found.")

def About(request):
    return render(request, 'blog/about.html')


def archive(request):
    article_list = Article.objects.order_by('-date_time')
    return render(request, 'blog/archive.html', {"article_list": article_list})


def Link(request):
    return render(request, 'blog/link.html')


def Message(request):
    try:
        info = base64.b64decode(request.GET['msg'])
        info = pickle.loads(info)
        data = "success"
    except Exception as e:
        data = "failed"
    return render(request, 'blog/message_board.html', {"source_id": "message","data":data})


@csrf_exempt
def GetComment(request):
    """
    接收畅言的评论回推， post方式回推
    :param request:
    :return:
    """
    arg = request.POST
    data = arg.get('data')
    data = json.loads(data)
    title = data.get('title')
    url = data.get('url')
    source_id = data.get('sourceid')
    if source_id not in ['message']:
        article = Article.objects.get(pk=source_id)
        article.commenced()
    comments = data.get('comments')[0]
    content = comments.get('content')
    user = comments.get('user').get('nickname')
    Comment(title=title, source_id=source_id, user_name=user, url=url, comment=content).save()
    return JsonResponse({"status": "ok"})


def detail(request, pk):
    """
    博文详情
    :param request:
    :param pk:
    :return:
    """
    article = get_object_or_404(Article, pk=pk)
    article.viewed()
    return render(request, 'blog/detail.html', {"article": article,
                                                "source_id": article.id})


def search(request):
    """
    搜索
    :param request:
    :return:
    """
    key = request.GET['key']
    article_list = Article.objects.filter(title__contains=key)
    return render(request, 'blog/search.html',
                  {"article_list": article_list, "key": key})


def tag(request, name):
    """
    标签
    :param request:
    :param name
    :return:
    """
    article_list = Article.objects.filter(tag__tag_name=name)
    return render(request, 'blog/tag.html', {"article_list": article_list,
                                             "tag": name})

def Hello(request):
    dat = request.GET['input'].replace('{',' ')
    template = 'Hello {user}, This is your input: ' + request.GET['input']

    return HttpResponse(template.format(user=request.user))
