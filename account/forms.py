#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/3/23 7:57
#@Author :weige
#@File :forms.py
from django import forms
from django.contrib.auth.models import User
from account.models import UserProfile,UserInfo
class LoginForm(forms.Form):
    user_name = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":" input-sm"}))
    user_password = forms.CharField(widget= forms.PasswordInput(attrs={"class":" input-sm"}),min_length=6,error_messages={'min_length':'提示:密码至少有6位'})

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password2",widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username","email")
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("password doesn`t match")
        return cd["password2"]



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone","birth")
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields =('user','school','company','address','profession','aboutme','photo')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)