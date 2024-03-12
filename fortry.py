import dash
from dash import html

# สร้างแอปพลิเคชัน Dash
app = dash.Dash(__name__)

# กำหนดเลเอาท์รวม
app.layout = html.Div([
    html.H1('หน้าโล่งๆ'),
    html.P('นี่คือหน้าที่ไม่มีเนื้อหาหรือเลเอาท์เพิ่มเติม')
])

if __name__ == '__main__':
    app.run_server(debug=True)
