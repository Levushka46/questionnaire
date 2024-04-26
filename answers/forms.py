from django.forms import Form
from django.forms import CharField, RadioSelect, CheckboxSelectMultiple


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
                ChoiceFieldClass = RadioSelect
                if question.multiple_choice:
                    ChoiceFieldClass = CheckboxSelectMultiple
                self.fields[f"question_{question.id}"] = ChoiceFieldClass(
                    label=question.text,
                    choices=[
                        (option.id, option.text)
                        for option in question.options.all()
                    ],
                    required=question.required,
                )
            if question.multiple_choice:
                self.fields[f"question_{question.id}"].widget.attrs[
                    "multiple"
                ] = True

    def _init_css_classes(self):
        for visible in self.visible_fields():
            widget = visible.field.widget
            if not isinstance(widget, (RadioSelect, CheckboxSelectMultiple)):
                widget.attrs['class'] = 'form-control'
