from django.contrib import admin

from .models import Page, Question, SelectOption


admin.site.register(Page)
admin.site.register(Question)
admin.site.register(SelectOption)
