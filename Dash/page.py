import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
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

# สร้างเลเอาท์สำหรับแต่ละเนื้อหาของแท็บ
tab1_layout = html.Div([
    html.H1('เนื้อหาของแท็บ 1'),
    html.Div('นี่คือเนื้อหาของแท็บ 1')
])

tab2_layout = html.Div([
    html.H1('เนื้อหาของแท็บ 2'),
    html.Div('นี่คือเนื้อหาของแท็บ 2')
])

# กำหนดรายการแท็บ
tabs = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='แท็บ 1', value='tab-1'),
        dcc.Tab(label='แท็บ 2', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

# กำหนด callback เพื่อเปลี่ยนเนื้อหาของแท็บ
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return tab1_layout
    elif tab == 'tab-2':
        return tab2_layout

# กำหนดเลเอาท์รวม
app.layout = html.Div([
    html.Div([
        html.P(children="📈", className="header-emoji"),
        html.H1(children="Dust forecast pm.5", className="header-title"),
        html.P(children="Analyze the air quality data", className="header-description"),
    ], className="header"),
    tabs
])

if __name__ == '__main__':
    app.run_server(debug=True)
