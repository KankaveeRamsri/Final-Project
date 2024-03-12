from dash import Dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import dash

import pandas as pd
import plotly.graph_objs as go

# Read data from CSV file
data = pd.read_csv("Clean_Data/Clean_data44t_Hatyai.csv")
data["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], format="%Y-%m-%d %H:%M:%S")
data.sort_values("DATETIMEDATA", inplace=True)

prediction = pd.read_csv("predict_WD_PM25.csv")
prediction["DATETIMEDATA"] = pd.to_datetime(prediction["DATETIMEDATA"], format="%Y-%m-%d")
prediction.sort_values("DATETIMEDATA", inplace=True)

# Define external stylesheets
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Air Quality Analytics: Understand Air Quality!"

navbar = html.Div(
    className="navbar",  # Added a class name for styling
    children=[
        html.Nav(
            className="nav",
            children=[
                html.A('DATA', href='/'),
                html.A('PREDICTION', href='/prediction'),
            ]
        )
    ]
)

# --------------------------------- Data layout --------------------------------- #
data_layout = html.Div(
    children=[
        navbar,
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="weather information", className="header-title"
                ),
                html.P(
                    children="Historical air quality data",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Parameter", className="menu-title"),
                        dcc.Dropdown(
                            id="parameter-filter-home",
                            options=[
                                {"label": param, "value": param}
                                for param in data.columns[2:]
                            ],
                            value="PM25",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range-home",
                            min_date_allowed=data["DATETIMEDATA"].min().date(),
                            max_date_allowed=data["DATETIMEDATA"].max().date(),
                            start_date=data["DATETIMEDATA"].min().date(),
                            end_date=data["DATETIMEDATA"].max().date(),
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Chart Type",
                            className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="chart-type-home",
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Scatter Plot", "value": "scatter"},
                            ],
                            value="line",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="chart-home", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="daily-stats-home", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className="menu-title"
                        ),
                        html.Div(
                            id="stats-table-home",
                            className="stats-table"
                        ),
                    ],
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ],
    className="nigga",
)

# --------------------------------- Prediction layout --------------------------------- #
predict_layout = html.Div(
    children=[
        navbar,
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="Forecast pm2.5 and wind direction", className="header-title"
                ),
                html.P(
                    children="Analyze the air quality data",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Parameter", className="menu-title"),
                        dcc.Dropdown(
                            id="parameter-filter-predict",
                            options=[
                                {"label": param, "value": param}
                                for param in prediction.columns[1:]
                            ],
                            value="PM25",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range-predict",
                            min_date_allowed=prediction["DATETIMEDATA"].min().date(),
                            max_date_allowed=prediction["DATETIMEDATA"].max().date(),
                            start_date=prediction["DATETIMEDATA"].min().date(),
                            end_date=prediction["DATETIMEDATA"].max().date(),
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Chart Type",
                            className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="chart-type-predict",
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Scatter Plot", "value": "scatter"},
                            ],
                            value="line",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="chart-predict", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className="menu-title"
                        ),
                        html.Div(
                            id="stats-table-predict",
                            className="stats-table"
                        ),
                    ],
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ],
    className="nigga",
)

# Define app callbacks

# Callback for updating statistics table for home layout
@app.callback(
    Output("stats-table-home", "children"),
    [
        Input("parameter-filter-home", "value"),
        Input("date-range-home", "start_date"),
        Input("date-range-home", "end_date"),
    ],
)
def update_stats_table_home(selected_parameter, start_date, end_date):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data.loc[mask]
    stats = filtered_data[selected_parameter].describe().reset_index().round(2)
    stats.columns = ["Statistic", "Value"]
    stats_table = dbc.Table.from_dataframe(stats, striped=True, bordered=True, hover=True, className="custom-table")
    
    title = html.Div(children=f"Statistics - {selected_parameter} ({start_date}-{end_date})", className="menu-title")
    
    return [title, stats_table]

# Callback for updating chart for home layout
@app.callback(
    Output("chart-home", "figure"),
    [
        Input("parameter-filter-home", "value"),
        Input("date-range-home", "start_date"),
        Input("date-range-home", "end_date"),
        Input("chart-type-home", "value"),
    ],
)
def update_chart_home(selected_parameter, start_date, end_date, chart_type):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data.loc[mask]
    
    if chart_type == "line":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "line",
        }
    elif chart_type == "scatter":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "mode": "markers",  # Scatter plot with markers
            "type": "scatter",
        }
    elif chart_type == "bar":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "bar",
        }
        
    layout = {
        "title": f"Air Quality Over Time - {selected_parameter}",
        "xaxis": {"title": "Datetime"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#17B897"],  # or any other color 
    }
    return {"data": [trace], "layout": layout}

# Callback for updating daily statistics chart for home layout
@app.callback(
    Output("daily-stats-home", "figure"),
    [
        Input("parameter-filter-home", "value"),
        Input("date-range-home", "start_date"),
        Input("date-range-home", "end_date"),
    ],
)
def update_daily_stats_home(selected_parameter, start_date, end_date):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data.loc[mask]

    # Group by date and calculate daily maximum, minimum, and mean values
    daily_stats = filtered_data.groupby(filtered_data["DATETIMEDATA"].dt.date)[selected_parameter].agg(['max', 'min', 'mean']).reset_index()

    # Create traces for each statistic
    traces = []
    for stat in ['max', 'min', 'mean']:
        traces.append(go.Scatter(
            x=daily_stats["DATETIMEDATA"],
            y=daily_stats[stat],
            mode='lines',
            name=stat.capitalize()  # Capitalize the statistic name for legend
        ))

    layout = {
        "title": f"Daily Statistics - {selected_parameter}",
        "xaxis": {"title": "Date"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#FF5733", "#33FF57", "#5733FF"],  # Different color for each statistic
    }

    return {"data": traces, "layout": layout}

# Callback for updating statistics table for prediction layout
@app.callback(
    Output("stats-table-predict", "children"),
    [
        Input("parameter-filter-predict", "value"),
        Input("date-range-predict", "start_date"),
        Input("date-range-predict", "end_date"),
    ],
)
def update_stats_table_predict(selected_parameter, start_date, end_date):
    mask = (
        (prediction["DATETIMEDATA"] >= start_date)
        & (prediction["DATETIMEDATA"] <= end_date)
    )
    filtered_data = prediction.loc[mask]
    stats = filtered_data[selected_parameter].describe().reset_index().round(2)
    stats.columns = ["Statistic", "Value"]
    stats_table = dbc.Table.from_dataframe(stats, striped=True, bordered=True, hover=True, className="custom-table")
    
    title = html.Div(children=f"Statistics - {selected_parameter} ({start_date}-{end_date})", className="menu-title")
    
    return [title, stats_table]

# Callback for updating chart for prediction layout
@app.callback(
    Output("chart-predict", "figure"),
    [
        Input("parameter-filter-predict", "value"),
        Input("date-range-predict", "start_date"),
        Input("date-range-predict", "end_date"),
        Input("chart-type-predict", "value"),
    ],
)
def update_chart_predict(selected_parameter, start_date, end_date, chart_type):
    mask = (
        (prediction["DATETIMEDATA"] >= start_date)
        & (prediction["DATETIMEDATA"] <= end_date)
    )
    filtered_data = prediction.loc[mask]
    
    if chart_type == "line":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "line",
        }
    elif chart_type == "scatter":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "mode": "markers",  # Scatter plot with markers
            "type": "scatter",
        }
    elif chart_type == "bar":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "bar",
        }
        
    layout = {
        "title": f"Air Quality Over Time - {selected_parameter}",
        "xaxis": {"title": "Datetime"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#17B897"],  # or any other color 
    }
    return {"data": [trace], "layout": layout}

# Callback for updating daily statistics chart for prediction layout

app.layout = html.Div([
    dcc.Location(id='url', refresh = False),
    html.Div(id = 'page-content'),
    dcc.Interval(id = 'interval-component',interval=60000)
])

@app.callback(Output('page-content', 'children'), 
            Input('url', 'pathname'),)
def display_page(pathname):
    if pathname == '/':
        return data_layout
    elif pathname == '/prediction':
        return predict_layout
    else:
        return '404 Page Not Found'

# Run the app if the script is executed directly
if __name__ == "__main__":
    app.run_server()
