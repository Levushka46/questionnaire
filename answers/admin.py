from django.contrib import admin

from .models import Answer, PageStack


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "get_question_page_title", "get_question_text", "answer")
    list_filter = ("user", "question")
    search_fields = ("user", "question", "answer")
    ordering = ("user", "question__page", "question__order", "id")
    list_select_related = ("user", "question", "question__page")

    def get_question_page_title(self, obj):
        return obj.question.page.title

    def get_question_text(self, obj):
        return obj.question.text


@admin.register(PageStack)
class PageStackAdmin(admin.ModelAdmin):
    list_display = ("user", "value")
    search_fields = ("user",)
