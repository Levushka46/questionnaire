from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from formpages.models import Question


UserModel = get_user_model()


class Answer(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="answers", verbose_name=_("user")
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers", verbose_name=_("question")
    )
    answer = models.CharField(_("answer"), max_length=255)


class PageStack(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="page_stack",
        verbose_name=_("user"),
    )
    value = models.CharField(_("value"), max_length=255)
