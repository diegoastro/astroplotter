# data_reader/views.py

from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile, FileColumn
from astropy.table import Table

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile(file=request.FILES['file'])
            uploaded_file.save()

            # Read the CSV file
            df = read.Table(uploaded_file.file.path)

            # Save the column names
            for column in df.columns:
                FileColumn.objects.create(file=uploaded_file, column_name=column)

            return redirect('data_reader:upload_success')
    else:
        form = UploadFileForm()
    return render(request, 'data_reader/upload.html', {'form': form})

def upload_success(request):
    return render(request, 'data_reader/upload_success.html')
