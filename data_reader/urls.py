
from django.urls import path
from .views import upload_file, upload_success

app_name = 'data_reader'

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('upload-success/', upload_success, name='upload_success'),
]