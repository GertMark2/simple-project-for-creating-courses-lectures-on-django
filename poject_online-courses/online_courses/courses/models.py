from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    """
    Модель курса.

    Хранит информацию о курсе, включая название, URL, описание, дату создания, автора и изображение.

    Поля:
    - title: Название курса
    - slug: Человекопонятный URL для курса (уникальный)
    - description: Описание курса
    - created_at: Дата и время создания курса (автоматически заполняется)
    - author: Автор курса (связь с моделью пользователя)
    - image: Изображение курса (опционально)
    """
    title = models.CharField(max_length=150, verbose_name="Название курса")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="URL курса")
    description = models.TextField(verbose_name="Описание курса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name="Автор курса")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name="Изображение курса")

    def __str__(self):
        return self.title


class Lecture(models.Model):
    """
    Модель лекции.

    Хранит информацию о лекциях, связанных с курсами.

    Поля:
    - course: Курс, к которому принадлежит лекция (связь с моделью Course)
    - title: Название лекции
    - video_url: URL видеоурока (опционально)
    - created_at: Дата и время создания лекции (автоматически заполняется)
    - order: Порядок лекции в курсе
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', verbose_name="Курс")
    title = models.CharField(max_length=150, verbose_name="Название лекции")
    video_url = models.URLField(max_length=200, verbose_name="URL видеоурока", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    order = models.PositiveIntegerField(verbose_name="Порядок лекции", help_text="Определяет порядок лекций в курсе", null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Comment(models.Model):
    """
    Модель комментария.

    Хранит информацию о комментариях, оставленных пользователями к лекциям.

    Поля:
    - lecture: Лекция, к которой относится комментарий (связь с моделью Lecture)
    - author: Автор комментария (связь с моделью пользователя)
    - text: Текст комментария
    - created_at: Дата и время создания комментария (автоматически заполняется)
    """
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='comments', verbose_name="Лекция")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор комментария")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.author} к {self.lecture.title}"

class Test(models.Model):
    """
    Модель теста.

    Хранит информацию о тестах, связанных с лекциями.

    Поля:
    - lecture: Лекция, к которой относится тест (связь с моделью Lecture)
    - question: Вопрос теста
    - correct_answer: Правильный ответ на тест
    - choices: Варианты ответов в формате JSON
    """
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='tests', verbose_name="Лекция")
    question = models.TextField(verbose_name="Вопрос")
    correct_answer = models.CharField(max_length=150, verbose_name="Правильный ответ")
    choices = models.JSONField(verbose_name="Варианты ответов", help_text="Введите варианты ответов в формате JSON")

    def __str__(self):
        return f"Тест для лекции {self.lecture.title}"
