from django.contrib import admin
from .models import Course, Lecture, Comment, Test

# Админка для модели Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Поля, которые будут отображаться в списке
    prepopulated_fields = {'slug': ('title',)}  # Автоматическое заполнение поля slug на основе title
    search_fields = ('title', 'author__username')  # Поля, по которым будет происходить поиск

# Админка для модели Lecture
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'order')  # Поля для отображения в списке
    list_filter = ('course', 'created_at')  # Фильтры по полям
    search_fields = ('title', 'course__title')  # Поля для поиска

# Админка для модели Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'lecture', 'created_at')  # Поля для отображения в списке
    list_filter = ('lecture', 'author')  # Фильтры по лекции и автору
    search_fields = ('author__username', 'lecture__title', 'text')  # Поля для поиска

# Админка для модели Test
class TestAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'question')  # Поля для отображения в списке
    list_filter = ('lecture',)  # Фильтр по лекции
    search_fields = ('question', 'lecture__title')  # Поля для поиска

# Регистрация моделей и соответствующих классов админки
admin.site.register(Course, CourseAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Test, TestAdmin)
