#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/4/20 9:58
#@Author :weige
#@File :list_views.py
import redis
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from articles.models import ArticleColumn,ArticlePost,ArticleTag
from course.models import Course
from django.conf import settings

from articles.forms import CommentForm
import MySQLdb

from articles import data_handle as data_handle
# 建立和redis的链接
r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)


def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        courses_of_user = Course.objects.filter(user = user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()
    #articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title, 4)
    page = request.GET.get('page')
    total_articles = ArticlePost.objects.count()
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request, "article/list/author_articles.html", {"articles":articles, "page":current_page, "userinfo":userinfo, "user":user,"courses_of_user":courses_of_user})
    tags = ArticleTag.objects.all()
    all_column = ArticleColumn.objects.all()
    return render(request, "article/list/article_titles.html", {"articles":articles, "page": current_page,'total_articles':total_articles,'tags':tags,"all_column":all_column})

def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id = id,slug = slug)
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking',article.id,1)
    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
    article_ranking_id = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_id))
    most_viewed.sort(key=lambda x:article_ranking_id.index(x.id))
    # 最新文章的排序
    latest_articles = ArticlePost.objects.order_by("-creat")[:5]
    most_comment_articles = ArticlePost.objects.annotate(total_comment=Count('comments')).order_by("-total_comment")[:5]

    # 执行插入流水操作
    # db = MySQLdb.connect("localhost", "root", "wjl984296155@#$", "laoqidjangobook", charset='utf8')
    # cursor = db.cursor()
    # article_id = id

    # print(request.user.id)
    # sql = "INSERT INTO account_view_count(user_id,article_id) VALUES ('%d','%d' )" % (int(request.user.id),int(article_id))
    # cursor.execute(sql)
    # db.commit()
    if request.method=="POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                new_comment.save()
    else:
        comment_form = CommentForm()
    article_tags_ids = article.article_tag.values_list("id", flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-creat')[:4]
    # 传入userid
    top_five_article_id = data_handle.recommend(request.user.id)
    # 输出recommend，article_id   list
    top_five_articles = []
    for i in range(len(top_five_article_id)):
        top_five_article = get_object_or_404(ArticlePost,id = top_five_article_id[i])
        top_five_articles.append(top_five_article)
    return render(request,'article/list/article_detail.html',{'article':article,'total_views':total_views,'most_viewed':most_viewed,'comment_form':comment_form,'latest_articles':latest_articles,'most_comment_articles':most_comment_articles,"similar_articles":similar_articles,"top_five_articles":top_five_articles})



@login_required(login_url="/account/login")
@csrf_exempt
@require_POST
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try :
            article = ArticlePost.objects.get(id = article_id)
            if action == 'like':
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("NO")


def get_same_tag_article(request,tag_id):
    all_column = ArticleColumn.objects.all()
    similar_articles = ArticlePost.objects.filter(article_tag__in=tag_id)
    total_articles = ArticlePost.objects.filter(article_tag__in=tag_id).count()
    tags = ArticleTag.objects.all()
    current_tag_name = ArticleTag.objects.get(id = tag_id)
    paginator = Paginator(similar_articles, 6)
    page = request.GET.get('page')
    # total_articles = ArticlePost.objects.count()
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,'article/list/article_titles.html',{'similar_articles':similar_articles,"tags":tags,"total_articles":total_articles,"page":current_page,"current_tag_name":current_tag_name,'all_column':all_column})



def get_same_column_article(request,column_id):
    column = ArticleColumn.objects.get(id = column_id)
    all_column = ArticleColumn.objects.all()
    same_column_articles = ArticlePost.objects.filter(column = column_id)
    total_articles = same_column_articles.count()
    current_column_name = ArticleColumn.objects.get(id = column_id)
    tags = ArticleTag.objects.all()

    paginator = Paginator(same_column_articles, 6)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    return render(request,'article/list/article_titles.html',{'same_column_articles':same_column_articles,"tags":tags,"total_articles":total_articles,"page":current_page,"current_column_name":current_column_name,'all_column':all_column})