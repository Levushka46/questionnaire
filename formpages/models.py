from django.db import models
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)


class Question(models.Model):

    class Types(models.TextChoices):
        TEXT = "line", _("single line text")
        SELECT = "select", _("select")

    text = models.CharField(_("question text"), max_length=255)
    type = models.CharField(
        _("question type"), max_length=32, choices=Types.choices, default=Types.TEXT
    )

    page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questions",
        verbose_name=_("page"),
    )
    order = models.PositiveSmallIntegerField(_("order on the page"), default=1)

    required = models.BooleanField(_("required"), default=False)
    multiple_choice = models.BooleanField(_("multiple choice"), default=False)


class SelectOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("question"),
    )
    text = models.CharField(_("option text"), max_length=255)
    order = models.PositiveSmallIntegerField(_("option order"), default=1)