from django.db.models import Q
from django.forms import Form, ValidationError
from django.forms import CharField, ChoiceField, EmailField, MultipleChoiceField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Answer, PageStack
from .widgets import RadioSelect, CheckboxSelectMultiple


User = get_user_model()


class PageForm(Form):
    template_name = "answers/form_snippet.html"

    def __init__(self, page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.next_page_id = None
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
        dynamic_next_pages = []
        for name, value in self.cleaned_data.items():
            if name.startswith("question_"):
                question_id = int(name.split("_")[1])
                question = self.page.questions.get(id=question_id)
                if isinstance(value, list):
                    answer = ", ".join(value)
                else:
                    answer = value
                answers.append(Answer(user=user, question_id=question_id, answer=answer))

                # Collect all dynamic next pages from the selected options
                if not isinstance(value, list):
                    value = [value]
                value = set(value)
                if question.type == "select":
                    options = question.options.all()
                    for option in options:
                        dyn_next_page = option.next_page_id
                        if dyn_next_page is not None and option.text in answer:
                            dynamic_next_pages.append(dyn_next_page)

        Answer.objects.bulk_create(answers)

        # Add page.next_page to the stack
        if self.page.next_page is not None:
            dynamic_next_pages.append(self.page.next_page.id)

        # Remove duplicates from the dynamic next pages
        unique_pages = set()
        new_stack = []
        for page in reversed(dynamic_next_pages):
            if page not in unique_pages:
                unique_pages.add(page)
                new_stack.append(page)

        # If there's still a stack, save it
        page_stack, _ = PageStack.objects.get_or_create(user=user)
        stack_value = page_stack.value
        if stack_value:
            stack = list(map(int, stack_value.split(",")))
        else:
            stack = []
        unique_pages = set(stack)
        for page_id in new_stack:
            if page_id not in unique_pages:
                stack.append(page_id)

        # The first stack entry is the next page
        if stack:
            self.next_page_id = stack.pop()

        page_stack.value = ",".join(map(str, stack))
        page_stack.save()

    def get_next_page_id(self):
        return self.next_page_id


class UserForm(UserCreationForm):
    email = EmailField(max_length=255)
    password = CharField()

    password1 = None
    password2 = None

    class Meta:
        model = get_user_model()
        fields = ("email",)


class SignInForm(UserForm):
    name = CharField(max_length=255)

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


class LoginForm(UserForm):
    pass
