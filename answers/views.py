from django.shortcuts import redirect, render, get_object_or_404
from django import forms
from django.contrib.auth import login, logout
from django.views import View

from answers.forms import PageForm, SignInForm
from answers.widgets import RadioSelect, CheckboxSelectMultiple
from formpages.models import Page


def page_dev(request):
    class TestForm(PageForm):
        question_1 = forms.CharField(label="Question 1?")
        question_radio = forms.ChoiceField(
            choices=[(1, "Option 1"), (2, "Option 2")],
            widget=RadioSelect,
        )
        question_checkboxes = forms.MultipleChoiceField(
            choices=[(1, "Option 1"), (2, "Option 2")],
            widget=CheckboxSelectMultiple,
        )
    form = TestForm(request.POST or None)
    page = {
        "title": "Page title",
        "description": "Page description",
    }
    return render(request, "answers/page.html", {"page": page, "form": form})


def page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    form = PageForm(page, request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # do something with the form data
            pass

    return render(request, "answers/page.html", {"page": page, "form": form})


def sign_in(request):
    return render(request, "answers/sign_in.html")


class SignInView(View):
    def get(self, request):
        logout(request)
        return render(request, "answers/sign_in.html")

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("page_dev")
        return render(request, "answers/sign_in.html", {"form": form})
