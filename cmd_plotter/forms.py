# cmd_plotter/forms.py

from django import forms
from data_reader.models import UploadedFile, FileColumn

class ColumnSelectionForm(forms.Form):
    uploaded_file = forms.ModelChoiceField(queryset=None)
    selected_columns = forms.MultipleChoiceField(choices=())

    def __init__(self, *args, **kwargs):
        uploaded_files = kwargs.pop('uploaded_files', None)
        super(ColumnSelectionForm, self).__init__(*args, **kwargs)
        
        if uploaded_files:
            self.fields['uploaded_file'].queryset = uploaded_files

    def set_choices(self, column_choices):
        self.fields['selected_columns'].choices = column_choices
