import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash import Dash
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.graph_objs as go

# Read data from CSV file
data = pd.read_csv("predict_day_WD.csv")
data["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], format="%Y-%m-%d")
data.sort_values("DATETIMEDATA", inplace=True)

# data2 = pd.read_csv("model_predictions.csv")
# data2["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], format="%Y-%m-%d %H:%M:%S")
# data2.sort_values("DATETIMEDATA", inplace=True)

# Define external stylesheets
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

# สร้างแอปพลิเคชัน Dash
app = dash.Dash(__name__)

# สร้างข้อมูล DataFrame ขึ้นมาเพื่อใช้เก็บข้อมูล
df = pd.DataFrame(columns=['Name', 'Age'])


# สร้างเลเอาท์สำหรับหน้าแรก
# Define page 1 layout
page_1_layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="Dust forecast pm.5", className="header-title"
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
                            id="parameter-filter",
                            options=[
                                {"label": param, "value": param}
                                for param in data.columns[1:]
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
                            id="date-range",
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
                            id="chart-type",
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
                        id="chart", config={"displayModeBar": False},
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
                        id="daily-stats", config={"displayModeBar": False},
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
                            id="stats-table",
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

# Callback for updating statistics table
@app.callback(
    Output("stats-table", "children"),
    [
        Input("parameter-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_stats_table(selected_parameter, start_date, end_date):
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

# Callback for updating chart
@app.callback(
    Output("chart", "figure"),
    [
        Input("parameter-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("chart-type", "value"),
    ],
)
def update_chart(selected_parameter, start_date, end_date, chart_type):
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

# Callback for updating daily statistics chart
@app.callback(
    Output("daily-stats", "figure"),
    [
        Input("parameter-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_daily_stats(selected_parameter, start_date, end_date):
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
# Define app callbacks

# Callbacks for page 1 components
# ...

# Define page 2 layout
page_2_layout = html.Div([
    html.H1('Page 2'),
    html.Div(id='display-data')
])

# Define app callbacks

# Callbacks for page 2 components
# ...

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the main app layout with tabs
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='page-1', children=[
        dcc.Tab(label='Page 1', value='page-1'),
        dcc.Tab(label='Page 2', value='page-2')
    ]),
    html.Div(id='tabs-content')
])

# Define callback to render content based on selected tab
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'page-1':
        return page_1_layout
    elif tab == 'page-2':
        return page_2_layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# สร้างเลเอาท์สำหรับหน้าที่สอง
page_2_layout = html.Div([
    html.H1('Page 2'),
    html.Div(id='display-data')
])

# ประกาศ callback สำหรับเพิ่มข้อมูล
@app.callback(
    Output('output-add-data', 'children'),
    [Input('add-button', 'n_clicks')],
    [State('name-input', 'value'),
     State('age-input', 'value')]
)
def add_data(n_clicks, name, age):
    if n_clicks > 0:
        global df
        df = df.append({'Name': name, 'Age': age}, ignore_index=True)
        return f'Data added: Name - {name}, Age - {age}'

# ประกาศ callback สำหรับแสดงข้อมูล
@app.callback(
    Output('display-data', 'children'),
    [Input('name-input', 'value'),
     Input('age-input', 'value')]
)
def display_data(name, age):
    global df
    return html.Table([
        html.Thead(
            html.Tr([html.Th('Name'), html.Th('Age')])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i]['Name']),
                html.Td(df.iloc[i]['Age'])
            ]) for i in range(len(df))
        ])
    ])

# กำหนดเลเอาท์หลักของแอปพลิเคชัน Dash
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='page-1', children=[
        dcc.Tab(label='Page 1', value='page-1'),
        dcc.Tab(label='Page 2', value='page-2')
    ]),
    html.Div(id='tabs-content')
])

# ประกาศ callback สำหรับเลือกหน้า
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'page-1':
        return page_1_layout
    elif tab == 'page-2':
        return page_2_layout
    
app.layout = html.Div(
    children=[
        html.P(children="📈", className="header-emoji"),
        html.H1(
            children="Dust forecast pm.5", className="header-title"
        ),
        html.P(
            children="Analyze the air quality data",
            className="header-description",
        ),
    ],
    className="header"
)


# เริ่มการทำงานของแอปพลิเคชัน Dash
if __name__ == '__main__':
    app.run_server(debug=True)
