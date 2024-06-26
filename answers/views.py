from django.shortcuts import redirect, render, get_object_or_404
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView

from answers.forms import LoginForm, PageForm, SignInForm
from answers.widgets import RadioSelect, CheckboxSelectMultiple
from formpages.models import Page, Survey


def page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    form = PageForm(page, request.POST or None, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            # do something with the form data
            pass

    return render(request, "answers/page.html", {"page": page, "form": form})


class PageView(LoginRequiredMixin, View):
    def get_page(self, page_id):
        return get_object_or_404(Page, id=page_id)

    def get_form(self, page, data=None, init_answers_from_user=None):
        return PageForm(page, data, user=init_answers_from_user)

    def get(self, request, page_id):
        page = self.get_page(page_id)
        form = self.get_form(page, init_answers_from_user=request.user)
        return render(request, "answers/page.html", {"page": page, "form": form})

    def post(self, request, page_id):
        page = self.get_page(page_id)
        form = self.get_form(page, request.POST, init_answers_from_user=request.user)
        if form.is_valid():
            form.save_answers(request.user)
            next_page_id = form.get_next_page_id()
            if next_page_id is not None:
                return redirect("page", page_id=next_page_id)
            else:
                return redirect("done")
        return render(request, "answers/page.html", {"page": page, "form": form})


class DoneView(TemplateView):
    template_name = "answers/done.html"


class NoSurveysView(TemplateView):
    template_name = "answers/no_surveys.html"


class SignInView(View):
    def get_start_page(self):
        survey = Survey.objects.filter(active=True).first()
        if survey is None:
            return "no_surveys", {}
        return "page", {"page_id": survey.first_page_id}

    def get(self, request):
        logout(request)
        return render(request, "answers/sign_in.html")

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            url_name, kwargs = self.get_start_page()
            return redirect(url_name, **kwargs)
        else:
            # If the email is correct, then try to log in user instead
            # name is optional in this case
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    url_name, kwargs = self.get_start_page()
                    return redirect(url_name, **kwargs)
                else:
                    form.add_error("password", "User exists, tried login: Invalid password.")
        return render(request, "answers/sign_in.html", {"form": form})
