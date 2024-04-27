from django.shortcuts import redirect, render, get_object_or_404
from django import forms
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView

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


class PageView(LoginRequiredMixin, View):
    def get_page(self, page_id):
        return get_object_or_404(Page, id=page_id)

    def get_form(self, page, data=None):
        return PageForm(page, data)

    def get(self, request, page_id):
        page = self.get_page(page_id)
        form = self.get_form(page)
        return render(request, "answers/page.html", {"page": page, "form": form})

    def post(self, request, page_id):
        page = self.get_page(page_id)
        form = self.get_form(page, request.POST)
        if form.is_valid():
            form.save_answers(request.user)
            next_page = page.next_page
            if next_page is not None:
                return redirect("page", page_id=next_page.id)
            else:
                return redirect("done")
        return render(request, "answers/page.html", {"page": page, "form": form})


class DoneView(TemplateView):
    template_name = "answers/done.html"


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
