from django.db import models
from django.utils.translation import gettext as _
from task_manager.users.models import Users
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(_("Name"), max_length=150, unique=True)
    description = models.TextField(_("Description"), blank=True)
    status = models.ForeignKey(
        Status,
        verbose_name=_("Status"),
        on_delete=models.PROTECT
    )
    author = models.ForeignKey(
        Users,
        verbose_name=_("Author"),
        on_delete=models.PROTECT,
        related_name="author",
        null=True
    )
    executor = models.ForeignKey(
        Users,
        verbose_name=_("Performer"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="executor"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label,
        through="LabelForTask",
        verbose_name=_('Labels'),
        blank=True
    )

    def __str__(self):
        return self.name


class LabelForTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    label = models.ForeignKey(Label, on_delete=models.PROTECT, null=True)
