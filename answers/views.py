from django.shortcuts import render, get_object_or_404

from formpages.forms import PageForm
from formpages.models import Page


def page_dev(request):
    return render(request, "answers/page.html")


def page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    form = PageForm(page, request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # do something with the form data
            pass

    return render(request, "answers/page.html", {"page": page, "form": form})
