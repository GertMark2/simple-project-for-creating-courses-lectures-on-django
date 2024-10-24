from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseForm, LectureForm, CommentForm, TestForm
from .models import Course, Lecture, Comment, Test
from django.views import View
from django.db.models import Max 
from django.core.paginator import Paginator 

# Класс-представление для регистрации пользователя
class UserRegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.
    Использует встроенную форму UserCreationForm.
    После успешной регистрации перенаправляет на страницу входа.
    """
    model = User
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

# Класс-представление для входа пользователя
class UserLoginView(LoginView):
    """
    Представление для входа пользователя.
    Перенаправляет аутентифицированных пользователей на список курсов.
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('course_list')

# Класс-представление для выхода пользователя
class UserLogoutView(LoginRequiredMixin, LogoutView):
    """
    Представление для выхода пользователя.
    После выхода перенаправляет на страницу входа.
    """
    next_page = reverse_lazy('login') 

# Список курсов
class CourseListView(ListView):
    """
    Представление для отображения списка курсов.
    Поддерживает пагинацию с количеством элементов на странице, равным 6.
    """
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 6  # Установите количество элементов на странице

    def get_context_data(self, **kwargs):
        """
        Добавляет объект страницы для использования в шаблоне.
        """
        context = super().get_context_data(**kwargs)
        context['page_obj'] = context['paginator'].get_page(self.request.GET.get('page'))
        return context

# Детали курса
class CourseDetailView(DetailView):
    """
    Представление для отображения деталей конкретного курса.
    """
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

# Создание курса (требует аутентификации)
class CourseCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового курса.
    Доступно только для аутентифицированных пользователей.
    Присваивает текущего пользователя в качестве автора курса.
    """
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'

    def form_valid(self, form):
        """
        Устанавливает автора курса перед его сохранением.
        """
        form.instance.author = self.request.user  # Присваиваем автору
        return super().form_valid(form)

    def get_success_url(self):
        """
        Перенаправляет на страницу деталей созданного курса.
        """
        return reverse_lazy('course_detail', kwargs={'slug': self.object.slug})

# Создание лекции (требует аутентификации)
class LectureCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой лекции.
    Доступно только для аутентифицированных пользователей.
    Привязывает лекцию к курсу и устанавливает порядок лекции.
    """
    model = Lecture
    form_class = LectureForm
    template_name = 'courses/lecture_form.html'

    def form_valid(self, form):
        """
        Устанавливает курс, к которому принадлежит лекция,
        и определяет порядок лекции.
        """
        form.instance.course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        
        # Получаем максимальное значение order для лекций в данном курсе
        max_order = Lecture.objects.filter(course=form.instance.course).aggregate(Max('order'))['order__max']
        
        # Устанавливаем значение order. Если max_order равно None, значит это первая лекция.
        form.instance.order = (max_order or 0) + 1
        return super().form_valid(form)

    def get_success_url(self):
        """
        Перенаправляет на страницу деталей курса после создания лекции.
        """
        return reverse_lazy('course_detail', kwargs={'slug': self.object.course.slug})

# Детали лекции
class LectureDetailView(View):
    """
    Представление для отображения деталей лекции, включая комментарии.
    Позволяет пользователям добавлять комментарии к лекции.
    """
    def get(self, request, lecture_id):
        """
        Обрабатывает GET-запрос для отображения деталей лекции и комментариев.
        """
        lecture = get_object_or_404(Lecture, id=lecture_id)
        comments_list = lecture.comments.all().order_by('-created_at')  # Получаем все комментарии и сортируем
        paginator = Paginator(comments_list, 10)  # Указываем количество комментариев на странице
        page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра
        comments = paginator.get_page(page_number)  # Получаем текущую страницу комментариев

        comment_form = CommentForm()
        return render(request, 'courses/lecture_detail.html', {
            'lecture': lecture,
            'comments': comments,
            'comment_form': comment_form
        })

    def post(self, request, lecture_id):
        """
        Обрабатывает POST-запрос для добавления нового комментария к лекции.
        """
        lecture = get_object_or_404(Lecture, id=lecture_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.lecture = lecture
            comment.author = request.user
            comment.save()
            return redirect('lecture_detail', lecture_id=lecture.id)

        # Если форма не валидна, показываем предыдущие комментарии
        comments_list = lecture.comments.all().order_by('-created_at')
        paginator = Paginator(comments_list, 10)
        page_number = request.GET.get('page')
        comments = paginator.get_page(page_number)

        return render(request, 'courses/lecture_detail.html', {
            'lecture': lecture,
            'comments': comments,
            'comment_form': comment_form
        })

# Создание теста (требует аутентификации)
class TestCreateView(View):
    """
    Представление для создания нового теста, привязанного к лекции.
    """
    def get(self, request, lecture_id):
        """
        Обрабатывает GET-запрос для отображения формы создания теста.
        """
        lecture = get_object_or_404(Lecture, id=lecture_id)
        form = TestForm()
        return render(request, 'courses/test_form.html', {'form': form, 'lecture': lecture})

    def post(self, request, lecture_id):
        """
        Обрабатывает POST-запрос для сохранения нового теста.
        """
        lecture = get_object_or_404(Lecture, id=lecture_id)
        form = TestForm(request.POST)

        if form.is_valid():
            test = form.save(commit=False)
            test.lecture = lecture  # Привязываем тест к лекции
            test.save()
            return redirect('lecture_detail', lecture_id=lecture.id)  # Перенаправляем на страницу лекции

        return render(request, 'courses/test_form.html', {'form': form, 'lecture': lecture})

# Отображение деталей теста
class TestDetailView(TemplateView):
    """
    Представление для отображения деталей теста, связанного с лекцией.
    """
    template_name = 'courses/test.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет тесты, связанные с лекцией, в контекст.
        """
        context = super().get_context_data(**kwargs)
        lecture_id = self.kwargs['lecture_id']
        context['tests'] = Test.objects.filter(lecture_id=lecture_id)
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает результаты теста, подсчитывает правильные ответы и отображает результаты.
        """
        lecture_id = self.kwargs['lecture_id']
        tests = Test.objects.filter(lecture_id=lecture_id)
        score = 0

        # Подсчет правильных ответов
        for test in tests:
            selected_answer = request.POST.get(f'question_{test.id}')
            if selected_answer == test.correct_answer:
                score += 1

        # Возвращение результатов теста
        return render(request, 'courses/test_results.html', {'score': score, 'total': tests.count()})

# Список тестов
class TestListView(ListView):
    """
    Представление для отображения списка всех тестов.
    """
    model = Test
    template_name = 'courses/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        """
        Возвращает все тесты.
        """
        return Test.objects.all()

# Редактирование теста
class TestEditView(UpdateView):
    """
    Представление для редактирования существующего теста.
    """
    model = Test
    form_class = TestForm
    template_name = 'courses/test_edit.html'

    def get_success_url(self):
        """
        Перенаправляет на страницу деталей теста после успешного редактирования.
        """
        return reverse_lazy('test_detail', kwargs={'pk': self.object.pk})


    
# class TestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Test
#     template_name = 'courses/test_confirm_delete.html'
#     success_url = reverse_lazy('course_list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['test'] = self.object
#         return context

#     def test_func(self):
#         test = self.get_object()
#         return self.request.user == test.autho