import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='My First Dashboard'),
    dcc.Graph(
        id='example',
        figure={
            'data': [
                {'x': [1, 2, 3, 4, 5], 'y': [7, 1, 7, 3, 4], 'type': 'line', 'name': 'Dorf'},
                {'x': [1, 2, 3, 4, 5], 'y': [1, 2, 3, 9, 5], 'type': 'bar', 'name': 'One'},
            ],
            'layout': {
                'title': 'Graph Example'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)