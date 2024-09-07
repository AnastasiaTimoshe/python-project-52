from .models import Status
from .forms import StatusForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(ListView):

    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusFormCreateView(SuccessMessageMixin, CreateView):

    form_class = StatusForm
    template_name = 'create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')
    extra_context = {'title': _('Create status'),
                     'target': 'status_create',
                     'action': _('Create')}


class StatusFormUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Status
    form_class = StatusForm
    template_name = 'update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status changed successfully')
    extra_context = {'action': _('Edit status')}


class StatusFormDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    extra_context = {'action': _('Delete status')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object().name
        return context

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if status.task_set.exists():
            messages.warning(request, _("Cannot delete status because it is in use"))
            return redirect(reverse_lazy('statuses'))
        else:
            return super().post(request, *args, **kwargs)
