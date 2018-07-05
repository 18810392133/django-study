from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from account.forms import LoginForm,RegistrationForm,UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from account.models import UserInfo,UserProfile
from django.contrib.auth.models import User
from account.forms import UserForm,UserInfoForm,UserProfileForm
import json
# Create your views here.

#
# def user_login(request):
#     if request.method == 'POST':
#         user_to_check = LoginForm(request.POST)
#         if user_to_check.is_valid():
#             data = user_to_check.cleaned_data
#             user = authenticate(username = data['user_name'],password = data['user_password'])
#             if user:
#                 login(request, user)
#                 return HttpResponseRedirect('/blog/')
#             else:
#                 print(user_to_check.errors)
#                 return render(request,'account/user_login.html',{'user_to_check':user_to_check})
#         else:
#             return render(request,'account/user_login.html',{'user_to_check':user_to_check})
#     else:
#         unlogin_user = LoginForm()
#         return render(request,'account/user_login.html',{"unlogin_user":unlogin_user})
#


def ajax_user_login(request):
    dic = {'status':True,'msg':None}
    if request.method == 'POST':
        print(request.POST['user_name'])
        user_to_check = LoginForm(request.POST)
        if user_to_check.is_valid():
            data = user_to_check.cleaned_data
            user = authenticate(username=data['user_name'], password=data['user_password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                # 有问题
                mes = '用户名或密码错误，请检查'
                dic['msg'] = mes
                dic['status'] = False
                # v =json.dumps(dic)
                return HttpResponse(dic['msg'])
        else:
            print(user_to_check.errors['user_password'][0])
            # return render(request, 'account/user_login.html', {'user_to_check': user_to_check})
            mes = user_to_check.errors['user_password'][0]
            dic['msg'] = mes
            dic['status'] = False
            return HttpResponse(dic['msg'])
    else:
        unlogin_user = LoginForm()
        return render(request,'account/user_login.html',{"unlogin_user":unlogin_user})


def register(request):
    if request.method == "POST":
        user_form_data = RegistrationForm(request.POST)
        user_profile_form_data  = UserProfileForm(request.POST)
        if user_form_data.is_valid()&user_profile_form_data.is_valid():
            new_form = user_form_data.save(commit = False)
            new_form.set_password(user_form_data.cleaned_data["password"])
            new_form.save()
            new_profile = user_profile_form_data.save(commit=False)
            new_profile.user = new_form
            new_profile.save()

            UserInfo.objects.create(user=new_form )
            return HttpResponse("successfully register ,you can <a href='{%url 'account:user_login'%}'>login now</a>")
        else:
            return HttpResponse("sorry")
    else:
        user_register_form = RegistrationForm()
        user_profile_form = UserProfileForm()
        return render(request,"account/register.html",{"user_register_form":user_register_form,"user_profile_form":user_profile_form})
@login_required(login_url='/account/login')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request,'account/myself.html',{'user':user,'userinfo':userinfo,'userprofile':userprofile})


@login_required(login_url='/account/login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user = request.user)
    userinfo = UserInfo.objects.get(user= request.user)
    if request.method == 'POST':
    #         取值
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if (user_form.is_valid() and userinfo_form.is_valid() and userinfo_form.is_valid()):
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userinfo.save()
            userprofile.save()
        return HttpResponseRedirect('/account/my-information')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth, "phone": userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school": userinfo.school, "company": userinfo.company, "profession": userinfo.profession,"address": userinfo.address, "aboutme": userinfo.aboutme})
        return render(request, "account/myself_edit.html",{"user_form": user_form, "userprofile_form": userprofile_form, "userinfo_form": userinfo_form})

@login_required(login_url='/account/login/')
def my_image(requset):
    if requset.method == 'POST':
        img = requset.POST['img']
        userinfo = UserInfo.objects.get(user = requset.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse('1')
    else:
        return render(requset,"account/imagecrop.html",)



