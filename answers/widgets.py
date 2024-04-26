from django.forms.widgets import RadioSelect as DjangoRadioSelect
from django.forms.widgets import CheckboxSelectMultiple as DjangoCheckboxSelectMultiple


class RadioSelect(DjangoRadioSelect):
    template_name = "answers/widgets/multiple_input.html"
    option_template_name = "answers/widgets/input_option.html"

    def optgroups(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " form-check-input"
        return super().optgroups(name, value, attrs)


class CheckboxSelectMultiple(DjangoCheckboxSelectMultiple):
    template_name = "answers/widgets/multiple_input.html"
    option_template_name = "answers/widgets/input_option.html"

    def optgroups(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " form-check-input"
        return super().optgroups(name, value, attrs)
