from django.urls import path
from task_manager.statuses.views import (
    IndexView,
    StatusFormCreateView,
    StatusFormUpdateView,
    StatusFormDeleteView
)


urlpatterns = [
    path('', IndexView.as_view(), name='statuses'),
    path('create/', StatusFormCreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', StatusFormUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', StatusFormDeleteView.as_view(), name='status_delete')
]
