import django_filters
from django import forms
from .models import Task
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):

    labels = django_filters.ModelChoiceFilter(
        label=_('Label'),
        null_label='Uncategorized',
        queryset=Label.objects.all(),
    )
    only_self_tasks = django_filters.BooleanFilter(
        label=_('Only self tasks'),
        widget=forms.CheckboxInput,
        method='show_users_tasks'
    )

    def show_users_tasks(self, queryset, author, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
