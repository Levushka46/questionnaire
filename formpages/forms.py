from django.forms import Form
from django.forms import CharField, RadioSelect, CheckboxSelectMultiple


class PageForm(Form):
    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for question in page.questions.all():
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
