from django.urls import path
from task_manager.labels.views import (
    IndexView,
    LabelFormCreateView,
    LabelFormUpdateView,
    LabelFormDeleteView
)


urlpatterns = [
    path('', IndexView.as_view(), name='labels'),
    path('create/', LabelFormCreateView.as_view(), name='label_create'),
    path('<int:pk>/update/', LabelFormUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', LabelFormDeleteView.as_view(), name='label_delete')
]
