from django.urls import path
from task_manager.tasks.views import (
    IndexView,
    TaskFormCreateView,
    TaskFormUpdateView,
    TaskFormDeleteView,
    TaskReadView
)


urlpatterns = [
    path('', IndexView.as_view(), name='tasks'),
    path('create/', TaskFormCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskFormUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskFormDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', TaskReadView.as_view(), name='task_read'),
]
