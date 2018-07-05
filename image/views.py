from braces.views import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.http import require_POST

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .forms import ImageForm
from .models import Image

# @login_required(login_url='/account/login/')
# @csrf_exempt
# @require_POST
# def upload_image(request):
#     # form = ImageForm(data=request.POST)
#     # if form.is_valid():
#     try:
#         # new_item = form.save(commit=False)
#         # new_item.user = request.user
#         img = request.POST["image"]
#         image_to_save = Image.objects.get(user_id=request.user.id)
#         image_to_save.image = img
#         image_to_save.title = request.POST["title"]
#         image_to_save.description = request.POST["description"]
#         image_to_save.save()
#         # new_item.save()
#         return HttpResponse("1")
#     except:
#         return HttpResponse("0")
class CreateDongtaiView(LoginRequiredMixin,CreateView):
    model = Image
    login_url = "/account/login/"
    def get(self, request , *args, **kwargs):
        form = ImageForm()
        return render(request, "image/manage/create_dongtai.html", {"form":form})
    def post(self, request,*args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_dongtai = form.save(commit=False)
            new_dongtai.user = request.user
            new_dongtai.save()
            return redirect("image:list_images")


@login_required(login_url='/account/login/')
def list_images(request):
    images = Image.objects.filter(user=request.user)


    paginator = Paginator(images, 6)
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
    return render(request, 'image/list_images.html', {"images": images,"page":current_page})


@login_required(login_url='/account/lobin/')
@require_POST
@csrf_exempt
def del_image(request):
    image_id = request.POST['image_id']
    try:
        image = Image.objects.get(id=image_id)
        image.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

def falls_images(request):
    images = Image.objects.all()
    return render(request, 'image/falls_images.html', {"images": images})

# 给动态点赞的函数

@login_required(login_url="/account/login")
@csrf_exempt
@require_POST
def like_dongtai(request):
    dongtai_id = request.POST.get("id")
    action = request.POST.get("action")
    if dongtai_id and action:
        try :
            dongtai = Image.objects.get(id = dongtai_id)
            if action == 'like':
                dongtai.users_like.add(request.user)
                return HttpResponse("1")
            else:
                dongtai.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("NO")

