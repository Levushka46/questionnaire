from django.test import TestCase

from django.contrib.auth import get_user_model

from answers.models import PageStack
from answers.forms import PageForm, SignInForm, LoginForm
from formpages.models import Page, Question, SelectOption


User = get_user_model()


class PageFormTest(TestCase):
    def test_page_form_init(self):
        form = PageForm()
        self.assertEqual(form.template_name, "answers/form_snippet.html")
        self.assertIsNone(form.page)
        self.assertIsNone(form.user)
        self.assertIsNone(form.next_page_id)
        self.assertEqual(form.fields, {})

    def test_page_form_init_with_page(self):
        page = Page.objects.create()
        form = PageForm(page=page)
        self.assertEqual(form.template_name, "answers/form_snippet.html")
        self.assertEqual(form.page, page)
        self.assertIsNone(form.user)
        self.assertIsNone(form.next_page_id)
        self.assertEqual(form.fields, {})

    def test_page_form_init_with_user(self):
        user = User.objects.create_user("testuser")
        form = PageForm(user=user)
        self.assertEqual(form.template_name, "answers/form_snippet.html")
        self.assertIsNone(form.page)
        self.assertEqual(form.user, user)
        self.assertIsNone(form.next_page_id)
        self.assertEqual(form.fields, {})

    def test_page_form_init_with_page_and_user(self):
        page = Page.objects.create()
        user = User.objects.create_user("testuser")
        form = PageForm(page=page, user=user)
        self.assertEqual(form.template_name, "answers/form_snippet.html")
        self.assertEqual(form.page, page)
        self.assertEqual(form.user, user)
        self.assertIsNone(form.next_page_id)
        self.assertEqual(form.fields, {})

    def test_page_form_init_fields(self):
        page = Page.objects.create()
        form = PageForm(page=page)
        self.assertEqual(form.fields, {})
        self.assertEqual(form.visible_fields(), [])

    def test_page_form_init_css_classes(self):
        page = Page.objects.create()
        form = PageForm(page=page)
        form._init_css_classes()
        for visible in form.visible_fields():
            widget = visible.field.widget
            self.assertEqual(widget.attrs, {"class": "form-control"})

    def test_page_form_save_answers(self):
        user = User.objects.create_user("testuser")
        page = Page.objects.create()
        form = PageForm(page, {})
        form.is_valid()
        form.save_answers(user)
        self.assertEqual(user.answers.count(), 0)

    def test_page_form_init_fields_with_questions(self):
        page = Page.objects.create()
        question = Question.objects.create(page=page, text="Test question")
        form = PageForm(page=page)
        self.assertEqual(len(form.fields), 1)
        self.assertEqual(form.visible_fields()[0].label, "Test question")

    def test_page_form_init_select_question(self):
        page = Page.objects.create()
        question = Question.objects.create(
            page=page, text="Test question", type="select"
        )
        option1 = SelectOption.objects.create(question=question, text="Option 1")
        option2 = SelectOption.objects.create(question=question, text="Option 2")
        form = PageForm(page=page)
        self.assertEqual(len(form.fields), 1)
        self.assertEqual(form.visible_fields()[0].label, "Test question")
        self.assertEqual(
            form.fields["question_1"].choices, [
                (option1.text, option1.text),
                (option2.text, option2.text),
            ]
        )

    def test_page_form_save_answers_with_answer(self):
        user = User.objects.create_user("testuser")
        page = Page.objects.create()
        question = Question.objects.create(page=page, text="Test question", type="line")
        form = PageForm(page, {f"question_{question.id}": "Answer"}, user=user)
        form.is_valid()
        form.save_answers(user)
        self.assertEqual(user.answers.count(), 1)
        answer = user.answers.first()
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.answer, "Answer")

    def test_page_form_save_answers_with_dyn_next_page(self):
        user = User.objects.create_user("testuser")
        page = Page.objects.create()
        next_page = Page.objects.create()
        question = Question.objects.create(
            page=page, text="Test question", type="select",
        )
        option = SelectOption.objects.create(question=question, text="Option", next_page=next_page)
        form = PageForm(page, {f"question_{question.id}": option.text}, user=user)
        form.is_valid()
        form.save_answers(user)
        self.assertEqual(user.answers.count(), 1)
        answer = user.answers.first()
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.answer, option.text)
        self.assertEqual(form.get_next_page_id(), next_page.id)

    def test_page_form_save_answers_with_dyn_stack(self):
        user = User.objects.create_user("testuser")
        orig_next_page = Page.objects.create()
        page = Page.objects.create(next_page=orig_next_page)
        next_page = Page.objects.create()
        question = Question.objects.create(
            page=page, text="Test question", type="select",
        )
        option = SelectOption.objects.create(question=question, text="Option", next_page=next_page)
        form = PageForm(page, {f"question_{question.id}": option.text}, user=user)
        form.is_valid()
        form.save_answers(user)
        self.assertEqual(user.answers.count(), 1)
        answer = user.answers.first()
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.answer, option.text)
        self.assertEqual(form.get_next_page_id(), next_page.id)
        stack = PageStack.objects.get(user=user)
        stack_value = stack.value.split(",")
        self.assertEqual(len(stack_value), 1)
        self.assertEqual(int(stack_value[0]), orig_next_page.id)


class SignInFormTest(TestCase):
    def test_sign_in_form_init_fields(self):
        form = SignInForm()
        self.assertEqual(len(form.fields), 3)
        self.assertEqual(form.visible_fields()[0].label, "Email")
        self.assertEqual(form.visible_fields()[1].label, "Password")
        self.assertEqual(form.visible_fields()[2].label, "Name")

    def test_sign_in_form_clean(self):
        data = {"email": "testuser@example.com", "password": "password", "name": "Test"}
        form = SignInForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean(), data)

    def test_sign_in_form_clean_invalid(self):
        data = {"email": "testuser@example.com"}
        form = SignInForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.clean(), data)


class LoginFormTest(TestCase):
    def test_login_form_init_fields(self):
        form = LoginForm()
        self.assertEqual(len(form.fields), 2)
        self.assertEqual(form.visible_fields()[0].label, "Email")
        self.assertEqual(form.visible_fields()[1].label, "Password")

    def test_login_form_clean(self):
        data = {"email": "testuser@example.com", "password": "password"}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean(), data)
