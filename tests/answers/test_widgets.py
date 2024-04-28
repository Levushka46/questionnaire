from django.test import TestCase

from answers.widgets import RadioSelect, CheckboxSelectMultiple


class RadioSelectTest(TestCase):
    def test_templates(self):
        self.assertEqual(RadioSelect.template_name, "answers/widgets/multiple_input.html")
        self.assertEqual(RadioSelect.option_template_name, "answers/widgets/input_option.html")

    def test_optgroups(self):
        radio_select = RadioSelect()
        name = "test"
        value = "test"
        attrs = {"class": "form-control"}
        optgroups = radio_select.optgroups(name, value, attrs)
        self.assertEqual(attrs, {"class": "form-control form-check-input"})


class CheckboxSelectMultipleTest(TestCase):
    def test_templates(self):
        self.assertEqual(CheckboxSelectMultiple.template_name, "answers/widgets/multiple_input.html")
        self.assertEqual(CheckboxSelectMultiple.option_template_name, "answers/widgets/input_option.html")

    def test_optgroups(self):
        checkbox_select_multiple = CheckboxSelectMultiple()
        name = "test"
        value = "test"
        attrs = {"class": "form-control"}
        optgroups = checkbox_select_multiple.optgroups(name, value, attrs)
        self.assertEqual(attrs, {"class": "form-control form-check-input"})
