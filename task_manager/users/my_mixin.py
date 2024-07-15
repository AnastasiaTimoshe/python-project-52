from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect


class MyLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.warning(self.request,
                             _("You are not logged in! Please log in.")
                             )
            return redirect(reverse_lazy('login'))
        return super().handle_no_permission()


class MyCheckPermissionMixin(UserPassesTestMixin):

    permission_message = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect('users_list')
