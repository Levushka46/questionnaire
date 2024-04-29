from django.db import models
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    next_page = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="previous_pages",
        verbose_name=_("next page"),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name=_("page")
        verbose_name_plural = _("pages")


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

    def __str__(self):
        return self.text

    class Meta:
        verbose_name=_("question")
        verbose_name_plural = _("questions")


class SelectOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("question"),
    )
    text = models.CharField(_("option text"), max_length=255)
    order = models.PositiveSmallIntegerField(_("option order"), default=1)
    next_page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="+",
        verbose_name=_("dynamic next page"),
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name=_("select option")
        verbose_name_plural = _("select options")


class Survey(models.Model):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    first_page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("first page"),
    )
    active = models.BooleanField(_("active"), default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name=_("survey")
        verbose_name_plural = _("surveys")
