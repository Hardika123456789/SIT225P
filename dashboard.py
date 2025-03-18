import dashboard
from dashboard import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("gyroscope_data.csv")

# Initialize Dash app
app = dashboard.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Gyroscope Data Dashboard", style={'textAlign': 'center'}),

    # Dropdown to select graph type
    html.Label("Select Graph Type:"),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Distribution Plot', 'value': 'histogram'}
        ],
        value='line'
    ),

    # Dropdown to select axis
    html.Label("Select Gyroscope Axis:"),
    dcc.Dropdown(
        id='axis-selector',
        options=[
            {'label': 'X-Axis', 'value': 'GyroX'},
            {'label': 'Y-Axis', 'value': 'GyroY'},
            {'label': 'Z-Axis', 'value': 'GyroZ'},
            {'label': 'All Axes', 'value': 'all'}
        ],
        value='all',
        multi=False
    ),

    # Text box for sample size
    html.Label("Enter Number of Samples to Display:"),
    dcc.Input(id='sample-size', type='number', value=100, min=10, step=10),

    # Buttons for navigation
    html.Div([
        html.Button("Previous", id="prev-btn", n_clicks=0),
        html.Button("Next", id="next-btn", n_clicks=0),
    ], style={'margin-top': '10px'}),

    # Graph output
    dcc.Graph(id='gyro-graph'),

    # Data Summary Table
    html.H3("Data Summary"),
    html.Div(id='data-summary')
])

# Variables to track the data slice
start_index = 0

# Callback to update the graph
@app.callback(
    Output('gyro-graph', 'figure'),
    Output('data-summary', 'children'),
    Input('graph-type', 'value'),
    Input('axis-selector', 'value'),
    Input('sample-size', 'value'),
    Input('prev-btn', 'n_clicks'),
    Input('next-btn', 'n_clicks')
)
def update_graph(graph_type, axis, sample_size, prev_clicks, next_clicks):
    global start_index

    # Adjust data slice based on navigation
    total_samples = len(df)
    start_index = max(0, min(start_index + (next_clicks - prev_clicks) * sample_size, total_samples - sample_size))
    data_slice = df.iloc[start_index:start_index + sample_size]

    # Select the appropriate graph type
    if axis == 'all':
        fig = px.line(data_slice, x="Time(ms)", y=["GyroX", "GyroY", "GyroZ"]) if graph_type == 'line' else \
              px.scatter(data_slice, x="Time(ms)", y=["GyroX", "GyroY", "GyroZ"]) if graph_type == 'scatter' else \
              px.histogram(data_slice, x=["GyroX", "GyroY", "GyroZ"])
    else:
        fig = px.line(data_slice, x="Time(ms)", y=axis) if graph_type == 'line' else \
              px.scatter(data_slice, x="Time(ms)", y=axis) if graph_type == 'scatter' else \
              px.histogram(data_slice, x=axis)

    # Generate data summary table
    summary = data_slice.describe().to_html()

    return fig, summary

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
