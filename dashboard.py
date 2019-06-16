import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import csv
import pandas
import pandas_datareader.data as web
import datetime as d
import plotly
import plotly.graph_objs as go
import random
from collections import deque

app=dash.Dash(__name__)

upfits_csv='fakefits.csv'

r=csv.reader(open(upfits_csv,"r"))

titles=[]
start_date=[]
end_date=[]
reach=[]
impression=[]
ctr=[]
cost=[]
clicks=[]
spent=[]
comments=[]
reactions=[]
shares=[]
video=[]
avg_time_watched=[]
video_plays=[]

for row in r:
    titles.append(row[0])
    start_date.append(row[1])
    end_date.append(row[2])
    reach.append(row[3])
    impression.append(row[4])
    ctr.append(row[5])
    cost.append(row[6])
    clicks.append(row[7])
    spent.append(row[8])
    comments.append(row[9])
    reactions.append(row[10])
    shares.append(row[11])
    video.append(row[12])
    avg_time_watched.append(row[18])
    video_plays.append(row[19])

data_dict={
    'titles':titles,
    'start_date':start_date,
    'end_date':end_date,
    'reach':reach,
    'impression':impression,
    'ctr':ctr,
    'cost':cost,
    'clicks':clicks,
    'spent':spent,
    'comments':comments,
    'reactions':reactions,
    'shares':shares,
    'video':video,
    'avg_time_wacthed':avg_time_watched,
    'video_plays':video_plays
}

for x in data_dict.values():
    del x[2]
    del x[8]

### Example of How a Graph Could Look -- Plotly and Dash

colors={
    'background':'#FFFFFF',
    'text':'#757575',
    'bar1':'#99cc00',
    'bar2':'#555555',
    'chart_bar':'#888888'
}

# data=[go.Bar(
#     x=data_dict['titles'][1:],
#     y=data_dict['spent'][1:],
#     text=data_dict['spent'][1:],
#     textposition='outside',
#     marker=dict(
#         color=colors['bar1'],
#         line=dict(
#             color=colors['chart_bar'],
#             width=1.5),
#             ),
#             opacity=.6
#             )]

# layout=go.Layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     xaxis=dict(
#         title='Campaign',
#         titlefont=dict(
#             family='Arial',
#             color=colors['text'],
#             size=24
#         ),
#         showticklabels=False),
#     yaxis=dict(
#         title='Amount Spent',
#         titlefont=dict(
#             family='Arial',
#             color=colors['text'],
#             size=24
#         ),
#         showticklabels=True
#     )
# )


# app.layout=html.Div(style={'backgroundColor': colors['background']}, children=[
#     html.H1(
#         children='Campaign Spending Graph',
#         style={
#             'textAlign':'center',
#             'color':colors['text'],
#             'font-family':'Arial'
#         }
#     ),
    
#     dcc.Graph(
#         id='example-graph',
#         figure={
#             'data':data,
#             'layout':layout
#                 }
#     )
#     ])

### Example of How a Graph Could Look -- Dash ###

# app.layout=html.Div(children=[
#     html.H1(children='Cost Graph'),

#     dcc.Graph(
#         id='example',
#         figure={
#             'data':[
#                 {'x':data_dict['titles'][1:], 'y':data_dict['cost'][1:], 'type':'bar', 'name':'Cost'}  
#             ],
#             'layout':{
#                 'title':'Cost'
#             }
#         }
#     )
# ])

### Actual Dashboard ###

app.layout=html.Div([
    html.Div([
        html.H1('Ford Upfits',
        style={'float':'left',
        }),
    ]),
    dcc.Dropdown(id='upfits-data',
        options=[{'label':s, 'value':s}
            for s in data_dict.keys()],
         value=['Cost per Result', 'Amount Spent', 'Reach'],
         multi=True
         ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-interval',
        interval=100,
        n_intervals=0),
], className='container', style={'width':'98%', 'margin-left':10, 'margin-right':10, 'max-width':500000})


# @app.callback(
#     dash.dependencies.Output('graphs', 'children'),
#     [dash.dependencies.Input('upfits-data','value')],
# )

@app.callback(
    Output('graphs','children'),
    [Input('upfits-data','value'), Input('graph-interval','n_intervals')]
)

def update_graph(data_name, n_interval):
    graphs=[]

    if len(data_name)>2:
        class_choice='col s12 m6 l4'
    elif len(data_name)==2:
        class_choice='col s12 m6 l6'
    else:
        class_choice='col s12'


    for x in data_name:
        data=[go.Bar(
            x=data_dict['titles'][1:],
            y=data_dict[data_name][1:],
            text=data_dict[data_name][1:],
            textposition='outside',
            marker=dict(
                color=colors['bar1'],
                line=dict(
                    color=colors['chart_bar'],
                    width=1.5),
                    ),
                    opacity=.6
                    )]

    layout=go.Layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        xaxis=dict(
            title='Campaign Name',
            titlefont=dict(
                family='Arial',
                color=colors['text'],
                size=24
                ),
                showticklabels=False),
                yaxis=dict(
                    title='{}'.format(data_name)
                    ,
                    titlefont=dict(
                        family='Arial',
                        color=colors['text'],
                        size=24
                        ),
                        showticklabels=True
                        ),
                margin={'l':50, 'r':1, 't':45, 'b':1}
                        )
        
        # data=go.Bar(
        #     x=data_dict['titles'][1:]
        #     y=data_dict[data_name]
        #     name='Graph'
        #     )
        
    graphs.append(html.Div(dcc.Graph(
            id=data_name,
            figure={'data':[data], 'layout': layout}
        )))


### Live Updates of Stocks -- Doesn't Work###

# X=deque(maxlen=20)
# Y=deque(maxlen=20)
# X.append(1)
# Y.append(1)

# app=dash.Dash(__name__)
# app.layout=html.Div([
#     dcc.Graph(id='live-graph', animate=True),
#     dcc.Interval(
#         id='graph-interval',
#         interval=100
#     )
# ])

# @app.callback(
#     Output('live-graph', 'figure'),
#     [Input('graph-interval', 'n_intervals')])

# def graph_updates():
#     X.append(X[-1]+1)
#     Y.append(Y[-1]+(Y[-1]*random.uniform(-0.1,0.1)))

#     data=go.Scatter(
#         x=list(X),
#         y=list(Y),
#         name='Live Scatterplot',
#         mode='lines+markers'
#     )

#     return {'data':[data], 'layout':go.Layout(xaxis=dict(range=[min(X),max(X)], \
#     yaxis=dict(min(Y),max(Y))))}


### Stock Lookup Dashboard ###

# app = dash.Dash(__name__)
# app.layout = html.Div(children=[
#     html.Div(children='Stock Dashboard'),
#     dcc.Input(id='input', value='', type='text'),
#     html.Div(id='output-graph')])

# @app.callback(
#     Output(component_id='output-graph', component_property='children'),
#     [Input(component_id='input', component_property='value')]
# )
# def make_graph(data):
#     start=d.datetime(2015,1,1)
#     end=d.datetime.now()
#     df = web.DataReader(data, 'yahoo', start, end)
#     return dcc.Graph(
#         id='example-graph',
#         figure={
#             'data':[
#                 {'x':df.index,'y':df.Close, 'type':'line', 'name':data},
#             ],
#             'layout':{'title':data}
#         }
#     )


### NOT MINE -- Dashboard with Live Updates

# X = deque(maxlen=20)
# X.append(1)
# Y = deque(maxlen=20)
# Y.append(1)

# app = dash.Dash(__name__)

# app.layout = html.Div(
#     [
#         dcc.Graph(id='live-graph', animate=True),
#         dcc.Interval(
#             id='graph-update',
#             interval=1000,
#             n_intervals = 0
#         ),
#     ]
# )

# @app.callback(Output('live-graph', 'figure'),
#         [Input('graph-update', 'n_intervals')])

# def update_graph_scatter(n):
#     X.append(X[-1]+1)
#     Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

#     data = plotly.graph_objs.Scatter(
#             x=list(X),
#             y=list(Y),
#             name='Scatter',
#             mode= 'lines+markers'
#             )

#     return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
#                                                 yaxis=dict(range=[min(Y),max(Y)]),)}

if __name__ == '__main__':
    app.run_server(debug=True)