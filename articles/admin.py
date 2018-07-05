from django.contrib import admin
from articles.models import ArticleColumn,ArticlePost,ArticleTag
# Register your models here.
class ArticleColumnAdmin(admin.ModelAdmin):
        list_display = ('user','column','created')
        list_filter = ('user','column','created')
class ArticlePostAdmin(admin.ModelAdmin):
        list_display = ('author', 'title', 'column','creat')
        list_filter = ('author', 'column','creat')
class ArticleTagAdmin(admin.ModelAdmin):
        list_display = ('tag','author')
        list_filter = ('author',)
admin.site.register(ArticleColumn,ArticleColumnAdmin)
admin.site.register(ArticlePost,ArticlePostAdmin)
admin.site.register(ArticleTag,ArticleTagAdmin)





