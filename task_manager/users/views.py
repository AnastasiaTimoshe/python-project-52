from .models import Users
from .forms import UserForm, UpdateUserForm
from .my_mixin import MyLoginRequiredMixin, MyCheckPermissionMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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
    extra_context = {'title': _('Registration'),
                     'target': 'user_create',
                     'action': _('Register')}


class UserFormUpdateView(MyLoginRequiredMixin,
                         MyCheckPermissionMixin,
                         SuccessMessageMixin,
                         UpdateView):

    model = Users
    form_class = UpdateUserForm
    template_name = 'update.html'
    success_url = reverse_lazy('users_list')
    success_message = _("The user has been successfully edited")
    permission_message = _("You do not have the rights to change another user.")
    extra_context = {'action': _('Edit user')}


class UserFormDeleteView(MyLoginRequiredMixin,
                         MyCheckPermissionMixin,
                         SuccessMessageMixin,
                         DeleteView):

    model = Users
    template_name = 'delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _("The user has been successfully deleted")
    login_message = _("You are not logged in! Please log in.")
    permission_message = _("You do not have the rights to delete another user.")
    extra_context = {'action': _('Delete user')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = f'{self.get_object().first_name} {self.get_object().last_name}'
        return context
