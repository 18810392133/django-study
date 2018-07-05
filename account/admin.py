from django.contrib import admin
from account.models import UserProfile,UserInfo
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ("phone",)
    list_display = ("user","birth","phone")
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user','school','company','profession','address','aboutme')
    list_filter = ('company','school','profession')
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserInfo,UserInfoAdmin)