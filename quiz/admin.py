from django.contrib import admin

from quiz.models import Category, Question, Quiz

admin.site.empty_value_display = '-пусто-'
admin.site.site_header = 'Панель управления QUIZE'
admin.site.site_title = 'QUIZE Admin'
admin.site.index_title = 'Управление контентом'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_editable = ('title',)
    search_fields = ('title',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_editable = ('title',)
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'quiz', 'category', 'difficulty')
    search_fields = ('text', 'description')
    list_filter = ('quiz', 'category', 'difficulty')
