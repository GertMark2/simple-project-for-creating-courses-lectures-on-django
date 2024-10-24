from django.urls import path
from .views import (
    UserRegisterView, UserLoginView, UserLogoutView,
    CourseListView, CourseDetailView, CourseCreateView,
    LectureCreateView, LectureDetailView,
    TestCreateView, TestListView, TestEditView,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Главная страница со списком курсов
    path('', CourseListView.as_view(), name='course_list'),

    # Аутентификация
    path('login/', UserLoginView.as_view(), name='login'),  # Страница входа
    path('logout/', UserLogoutView.as_view(), name='logout'),  # Страница выхода
    path('register/', UserRegisterView.as_view(), name='register'),  # Страница регистрации

    # Создание курса
    path('course/create/', CourseCreateView.as_view(), name='course_create'),  # Страница создания курса
    
    # Динамические маршруты для курсов и лекций
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),  # Страница подробной информации о курсе
    path('course/<slug:course_slug>/lecture/create/', LectureCreateView.as_view(), name='lecture_create'),  # Страница создания лекции
    path('lecture/<int:lecture_id>/', LectureDetailView.as_view(), name='lecture_detail'),  # Страница подробной информации о лекции
    
    # Комментарии к лекции
    path('lecture/<int:lecture_id>/comment/', LectureDetailView.as_view(), name='lecture_comment'),  # Обработка комментариев к лекции

    # Управление тестами
    path('lecture/<int:lecture_id>/test/create/', TestCreateView.as_view(), name='test_create'),  # Страница создания теста
    path('lecture/<int:lecture_id>/test/', TestListView.as_view(), name='test_list'),  # Страница списка тестов
    path('test/<int:test_id>/edit/', TestEditView.as_view(), name='test_edit'),  # Страница редактирования теста
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
