from django.test import TestCase, Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from answers.views import PageView, DoneView, SignInView
from formpages.models import Page


User = get_user_model()


class PageViewTest(TestCase):
    def setUp(self):
        self.page = Page.objects.create()
        self.user = User.objects.create_user("testuser")
        self.client = Client()
        self.client.force_login(self.user)

    def test_get_page(self):
        page_view = PageView()
        page = page_view.get_page(self.page.id)
        self.assertEqual(page, self.page)

    def test_get_form(self):
        page_view = PageView()
        form = page_view.get_form(self.page, init_answers_from_user=self.user)
        self.assertEqual(form.page, self.page)
        self.assertEqual(form.user, self.user)

    def test_get(self):
        response = self.client.get(f"/page/{self.page.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "answers/page.html")

    def test_post(self):
        response = self.client.post(f"/page/{self.page.id}/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("done"))
