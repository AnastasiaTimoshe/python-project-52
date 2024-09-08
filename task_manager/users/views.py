from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Users
from .forms import UserForm, UpdateUserForm
from task_manager.tasks.models import Task


class IndexView(ListView):
    model = Users
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserFormCreateView(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UserForm
    template_name = 'create.html'
    success_url = reverse_lazy('login')
    success_message = _("The user has been successfully registered")

    extra_context = {
        'title': _('Registration'),
        'target': 'user_create',
        'action': _('Register')
    }


class UserFormUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UpdateUserForm
    template_name = 'update.html'
    success_url = reverse_lazy('users_list')
    success_message = _("The user has been successfully edited")
    permission_message = _("You do not have the rights to change another user.")
    login_message = _("You are not logged in! Please log in.")

    extra_context = {'action': _('Edit user')}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.login_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.cleaned_data.get('password1'):
            self.object.set_password(form.cleaned_data['password1'])
            self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect('users_list')


class UserFormDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Users
    template_name = 'delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _("The user has been successfully deleted")
    login_message = _("You are not logged in! Please log in.")
    permission_message = _("You do not have the rights to delete another user.")

    extra_context = {'action': _('Delete user')}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.login_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = f'{self.get_object().first_name} {self.get_object().last_name}'
        return context

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect('users_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_in_use = Task.objects.filter(
            Q(executor=self.object) | Q(author=self.object)
        ).exists()

        if user_in_use:
            messages.error(
                self.request,
                _("Cannot delete user because they are in use")
            )
            return redirect(self.success_url)

        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request,
                _("It is not possible to delete a user because it is being used")
            )
            return redirect(self.success_url)
