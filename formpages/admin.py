from django.contrib import admin

from .models import Page, Question, SelectOption


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "next_page")
    search_fields = ("title", "description")
    inlines = [QuestionInline]


class SelectOptionInline(admin.StackedInline):
    model = SelectOption
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("page", "order", "text", "type", "required", "multiple_choice")
    list_filter = ("type", "page", "required", "multiple_choice")
    search_fields = ("text",)
    ordering = ("page", "order")
    inlines = [SelectOptionInline]


@admin.register(SelectOption)
class SelectOptionAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "text", "next_page")
    list_filter = ("question",)
    search_fields = ("text",)
    ordering = ("question", "order")
