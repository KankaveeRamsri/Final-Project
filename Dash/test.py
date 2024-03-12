import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# หน้าเว็บที่หน้าแรก
page_1_layout = html.Div([
    html.H1('หน้าแรก'),
    html.Div('นี่คือหน้าแรก')
])

# หน้าเว็บที่สอง
page_2_layout = html.Div([
    html.H1('หน้าสอง'),
    html.Div('นี่คือหน้าสอง')
])

# ระบุเส้นทางสำหรับการแสดงหน้า
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return 'ไม่พบหน้าที่คุณต้องการ'

if __name__ == '__main__':
    app.run_server(debug=True)
