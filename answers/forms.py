from django.db.models import Q
from django.forms import Form, ValidationError
from django.forms import CharField, ChoiceField, EmailField, MultipleChoiceField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Answer
from .widgets import RadioSelect, CheckboxSelectMultiple


User = get_user_model()


class PageForm(Form):
    template_name = "answers/form_snippet.html"

    def __init__(self, page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        if page is not None:
            self._init_fields()
        self._init_css_classes()

    def _init_fields(self):
        for question in self.page.questions.all():
            if question.type == "line":
                self.fields[f"question_{question.id}"] = CharField(
                    label=question.text, required=question.required
                )
            elif question.type == "select":
                ChoiceFieldClass = ChoiceField
                ChoiceWidgetClass = RadioSelect
                if question.multiple_choice:
                    ChoiceFieldClass = MultipleChoiceField
                    ChoiceWidgetClass = CheckboxSelectMultiple
                self.fields[f"question_{question.id}"] = ChoiceFieldClass(
                    label=question.text,
                    choices=[
                        (option.text, option.text)
                        for option in question.options.all()
                    ],
                    required=question.required,
                    widget=ChoiceWidgetClass,
                )

    def _init_css_classes(self):
        for visible in self.visible_fields():
            widget = visible.field.widget
            if not isinstance(widget, (RadioSelect, CheckboxSelectMultiple)):
                widget.attrs['class'] = 'form-control'

    def save_answers(self, user):
        answers = []
        for name, value in self.cleaned_data.items():
            if name.startswith("question_"):
                question_id = int(name.split("_")[1])
                if isinstance(value, list):
                    answer = ", ".join(value)
                else:
                    answer = value
                answers.append(Answer(user=user, question_id=question_id, answer=answer))
        Answer.objects.bulk_create(answers)

    def get_next_page_id(self):
        next_page = self.page.next_page
        return next_page.id if next_page is not None else None


class SignInForm(UserCreationForm):
    name = CharField(max_length=255)
    email = EmailField(max_length=255)
    password = CharField()

    password1 = None
    password2 = None

    class Meta:
        model = get_user_model()
        fields = ("email",)

    def _post_clean(self):
        super()._post_clean()
        email = self.cleaned_data.get("email")
        if User.objects.filter(Q(email=email) | Q(username=email)).exists():
            e = ValidationError("User with this email already exists.")
            self.add_error("email", e)

    def save(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        return User.objects.create_user(
            email, email=email, password=password, first_name=self.cleaned_data["name"],
        )
