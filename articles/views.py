from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from django.contrib.auth.models import User
from articles.models import ArticleColumn, ArticlePost, ArticleTag
from articles.forms import ArticleColumnForm, ArticlePostForm, ArticleTagForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json
# Create your views here.

@csrf_exempt
@login_required(login_url='/account/login/')
def article_column(request):
    if request.method =="GET":#点击栏目管理连接时
        columns = ArticleColumn.objects.filter(user = request.user)#将用户所属的栏目都列举出来
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {'columns':columns,'column_form':column_form})
    else:
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column = column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user_id=request.user.id,column = column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
    #     取得id所对应的对象
        item = ArticleColumn.objects.get(id = column_id)
        item.column = column_name
        item.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]
    try:
    #     取得id所对应的对象
        item = ArticleColumn.objects.get(id = column_id)
        item.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    if request.method =="POST":
        article_post_from = ArticlePostForm(data=request.POST)
        if article_post_from.is_valid():
            cd = article_post_from.cleaned_data
            try:
                new_article = article_post_from.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id = request.POST["column_id"])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_from = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request,"article/column/article_post.html",{"article_post_from":article_post_from,"article_columns":article_columns,'article_tags':article_tags})

@login_required(login_url="/account/login")
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles,6)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        article_list = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        article_list = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        article_list = current_page.object_list
    return render(request,"article/column/article_list.html",{"articles":article_list,"page":current_page})

@login_required(login_url="/account/login")
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,"article/column/article_detail.html",{"content":article})

@login_required(login_url="/account/login")
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        aticle = ArticlePost.objects.get(id = article_id)
        aticle.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')

@login_required(login_url="/account/login")
@csrf_exempt
def reedit_article(request,article_id):
    if request.method == 'GET':
        all_column = request.user.article_column.all()
        article = ArticlePost.objects.get(id = article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title})
        this_article_column = article.column
        article_tags = request.user.tag.all()
        return render(request,'article/column/reedit_article.html',{'all_column':all_column,'article':article,'this_article_column':this_article_column,'this_article_form':this_article_form,'article_tags':article_tags})
    else:
        reedit_article = ArticlePost.objects.get(id = article_id)
        try:
            reedit_article.column = request.user.article_column.get(id = request.POST["column_id"])
            reedit_article.title = request.POST["title"]
            reedit_article.body = request.POST["body"]
            reedit_article.save()
            tags = request.POST['tags']
            if tags:
                for atag in json.loads(tags):
                    tag = request.user.tag.get(tag=atag)
                    reedit_article.article_tag.add(tag)
            return HttpResponse("1")
        except:
            return HttpResponse("2")

@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, "article/tag/tag_list.html", {"article_tags":article_tags, "article_tag_form":article_tag_form})
    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        print(request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                print(new_tag)
                new_tag.save()
                return HttpResponse(new_tag)
            except:
                return HttpResponse("the data cannot be save.")
        else:
            return HttpResponse("sorry, the form is not valid.")



@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
    	return HttpResponse("2")
