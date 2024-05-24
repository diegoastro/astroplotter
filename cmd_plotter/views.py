# cmd_plotter/views.py

from django.shortcuts import render
from data_reader.models import UploadedFile, FileColumn
from astropy.table import Table
import plotly.graph_objects as go

def plot_cmd(request):
    uploaded_files = UploadedFile.objects.all()
    form = ColumnSelectionForm(request.POST or None, uploaded_files=uploaded_files)
    plot_div = None

    if request.method == 'POST' and form.is_valid():
        uploaded_file_id = form.cleaned_data['uploaded_file']
        selected_columns = form.cleaned_data['selected_columns']

        # Fetch the uploaded file
        uploaded_file = UploadedFile.objects.get(pk=uploaded_file_id)
        file_path = uploaded_file.file.path

        # Read the file using astropy.table.Table
        data_table = Table.read(file_path, format='ascii')

        # Ensure the selected columns exist in the table
        if not all(column in data_table.colnames for column in selected_columns):
            return render(request, 'cmd_plotter/error.html', {'error': 'Selected columns do not exist in the table'})

        # Plot the CMD using the selected columns
        fig = go.Figure()

        # Add the CMD scatter plot
        fig.add_trace(go.Scatter(
            x=data_table[selected_columns[0]],  # X-axis column
            y=data_table[selected_columns[1]],  # Y-axis column
            mode='markers',
            # Customize marker attributes as needed
            marker=dict(
                size=5,
                color=data_table[selected_columns[2]],  # Color column
                colorscale='Rainbow',
                colorbar=dict(title='log(M)'),
                showscale=True,
                reversescale=True
            ),
            hovertemplate=f'{selected_columns[2]}: %{{x}}<br>{selected_columns[1]}: %{{y}}<extra></extra>',
            name='CMD'
        ))

        # Update layout
        fig.update_layout(
            title='Color-Magnitude Diagram (CMD)',
            xaxis_title=selected_columns[0],
            yaxis_title=selected_columns[1],
            height=600,
            width=800
        )

        # Get the HTML representation of the plot
        plot_div = fig.to_html(full_html=False)

    return render(request, 'cmd_plotter/cmd_plot.html', {'form': form, 'plot_div': plot_div})
