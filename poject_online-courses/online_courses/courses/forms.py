from django import forms
from .models import Course, Lecture, Comment, Test

class CourseForm(forms.ModelForm):
    """
    Форма для создания или редактирования курса.
    Использует модель Course и позволяет вводить следующие поля:
    - title: Заголовок курса
    - slug: Человекопонятный URL для курса
    - description: Описание курса
    - image: Изображение курса (по желанию)
    """
    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'image']  # Добавьте поле slug, если необходимо

class LectureForm(forms.ModelForm):
    """
    Форма для создания или редактирования лекции.
    Использует модель Lecture и позволяет вводить следующие поля:
    - title: Заголовок лекции
    - video_url: URL видео лекции
    - order: Порядок лекции в курсе
    """
    class Meta:
        model = Lecture
        fields = ['title', 'video_url', 'order']
        
    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с установкой значения по умолчанию для поля order.
        """
        super().__init__(*args, **kwargs)
        self.fields['order'].initial = 1  # Устанавливаем значение по умолчанию для поля order

class CommentForm(forms.ModelForm):
    """
    Форма для добавления комментария к лекции.
    Использует модель Comment и позволяет вводить следующее поле:
    - text: Текст комментария
    """
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),  # Устанавливаем количество строк для текстового поля
        }

class TestForm(forms.ModelForm):
    """
    Форма для создания или редактирования теста.
    Использует модель Test и позволяет вводить следующие поля:
    - question: Вопрос теста
    - correct_answer: Правильный ответ на тест
    - choices: Варианты ответов в формате JSON
    """
    class Meta:
        model = Test
        fields = ['question', 'correct_answer', 'choices']

    def clean_choices(self):
        """
        Проверяет, что поле choices не пустое и имеет правильный формат JSON.
        Возвращает список вариантов ответов.
        """
        choices = self.cleaned_data.get('choices')
        if not choices:
            raise forms.ValidationError("Это поле не может быть пустым.")
        try:
            import json
            choices = json.loads(choices)
            if not isinstance(choices, list) or len(choices) < 2:
                raise forms.ValidationError("Введите как минимум два варианта ответа.")
        except json.JSONDecodeError:
            raise forms.ValidationError("Введите варианты ответов в формате JSON.")
        return choices
