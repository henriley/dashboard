import dash
# import dash_auth
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import csv
import pandas as pd
import plotly
import plotly.graph_objs as go
import base64
import flask
# from dash_google_auth import GoogleOAuth

# VALID_USERNAME_PASSWORD_PAIRS = {
#     'henriley': '1234'
# }

### CSS that allows for real time updates of the grpahs and charts ###

external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]
external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js",
                  'https://pythonprogramming.net/static/socialsentiment/googleanalytics.js']

### Initializes the app to start running ###

app=dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

### Makes app dash app run locally on your computer ###

app.css.config.serve_locally=True
app.scripts.config.serve_locally=True
app.config['suppress_callback_exceptions']=True

## Loads in the CSV of the data ###

df=pd.read_csv('fakefits.csv').rename(columns={'Unnamed: 0':'Title'}).drop([1, 8]).fillna('NONE').to_dict('records')

campaign_dict={}

campaign_dict['Campaign 1']=df[0]
campaign_dict['Campaign 2']=[
    df[1], df[2], df[3], df[4], df[5], df[6]]
campaign_dict['Campaign 3']=[
    df[7], df[8]]

campaigns_list=[
    'Campaign 1']

camp_1_keys=[x for x in campaign_dict['Campaign 1'].keys()][:12]
camp_1_values=[x for x in campaign_dict['Campaign 1'].values()][:12]
del camp_1_keys[0:3]
del camp_1_values[0:3]

# camp_2_keys=[x for x in campaign_dict['Campaign 2'].keys()][:12]
# camp_2_values=[x for x in campaign_dict['Campaign 2'].values()][:12]
# del camp_2_keys[0:3]
# del camp_2_values[0:3]

# camp_3_keys=[x for x in campaign_dict['Campaign 3'].keys()][:12]
# camp_3_values=[x for x in campaign_dict['Campaign 3'].values()][:12]
# del camp_3_keys[0:3]
# del camp_3_values[0:3]

### These are the company colors used throughout branding. Use them for the styling of the graphs, charts, and labels ###

colors={
    'background':'#FFFFFF',
    'text':'#757575',
    'bar1':'#99cc00',
    'bar2':'#555555',
    'chart_bar':'#888888'
}

### Actual Dashboard ###

image_filename='images/OneMagnify_logo_stacked_green_gray_rgb.png' ### Replace with your own image ###
encoded_image=base64.b64encode(open(image_filename, 'rb').read())


### This creates the header and inserts the OneMagnify logo ###

app.layout=html.Div([
    html.Div([
        html.Span("Ford Upfits", className='app-title'),
        html.Div(
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), className='om-logo'))],
        className="row header"),

### Creates the tabs that allow you to switch between the different metrics (Email, Social Media, Website, Direct Mail) ###

    dcc.Tabs(
        id="tabs",
        value='social_media_tab',
        parent_className='custom-tabs',
        className='tabs-container',
        children=[
            dcc.Tab(label="Social Media",
                    value="social_media_tab",
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                    ),
            dcc.Tab(label="Email",
                    value="email_tab",
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                    ),
            dcc.Tab(label="Direct Mail",
                    value="direct_mail_tab",
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                    ),
        ]),
    html.Div(id='tabs-content-classes')])

### Wrapper that populates each of the tabs with the correct information ###

@app.callback(
    Output('tabs-content-classes', 'children'),
    [Input('tabs', 'value')]
)

def render_content(tab):
    if tab=="social_media_tab":
        return html.Div([
            dcc.Markdown('''
#### FCC Social Key Insights

* 1) 3 Social Campaigns launched in Q1 - Transit Upfit Incentive, FordUpfits.com Announcement and Spring CVS							
* 2) 18 sales can be attributed to the Q1 social campaigns							
* 3) Q1 social ads reached 375,514 users, delivered 1.8M impressions, and had an average CTR of 3.06%							
* 4) The RV-Interests-Recreational and Handraisers w/Lookalikes-Recreation social ads had the highest CTRs in Q1							
* 5) The Handraisers w/Lookalikes-Recreation social ad also received the most user engagement with 22 comments, 341 reactions, and 76 shares							
* 6) The 2018 FTT social ads received over 3 million impressions and had a collective reach of over 600k and an average CTR of 1.25%							
* 7) With last year's metrics in mind, the 2019 social campaigns are tracking to exceed the number of impressions and reach received in 2018
''', className='markdown-social'),
            dcc.Dropdown(
                    id='upfits-data',
                    options=[{'label':s, 'value':s}
                    for s in campaigns_list],
                    value=['Campaign 1'],
                    multi=True,
                    className='dropdown'
                    ),
            html.Div(
                    children=html.Div(
                    id='bar-graphs'),
                    className='row'),
            
            dcc.Interval(
                    id='graph-interval',
                    interval=1*1000,
                    n_intervals=0),
                    ], 
                className='container')
    if tab=="email_tab":
        return html.Div([
            html.H1('HI REMA')])
    if tab=="direct_mail_tab":
        return html.Div([
            html.H1('HI MEAGEN')])

### Wrapper that goes through the IDs of each graph, and updates them over time -- this is what allows the graphs to be real time or respond to user input ###

@app.callback(
    Output('bar-graphs','children'),
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
        if x=='Campaign 1':
            data=[go.Bar(
                x=camp_1_keys,
                y=camp_1_values,
                text=camp_1_values,
                textposition='outside',
                marker=dict(
                    color=colors['bar1'],
                    line=dict(
                        color=colors['chart_bar'],
                        width=1.5),
                        ),
                opacity=.6)]

            layout=go.Layout(
                height=500,
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                title=dict(
                    text='Campaign 1',
                    xref='paper',
                    x=0),
                xaxis=dict(
                    title='Metric Name',
                    titlefont=dict(
                        family='Arial',
                        color=colors['text'],
                        size=24),
                        showticklabels=False),
                yaxis=dict(
                    title='Number',
                    titlefont=dict(
                        family='Arial',
                        color=colors['text'],
                        size=24),
                        showticklabels=True),
                margin={'l':60,'r':10,'t':45})

            graphs.append(html.Div(dcc.Graph(
                    id=x,
                    animate=False,
                    figure={'data':data, 'layout': layout}
                ), className=class_choice))

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)
