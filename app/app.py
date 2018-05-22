from flask import Flask, send_from_directory
from clustering import *
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import logging

server = Flask('Clustering dashboard', static_url_path='')

# Hack to allow serving custom CSS. Taken from this:
# https://community.plot.ly/t/how-do-i-use-dash-to-add-local-css/4914/4
@server.route('/static/style.css')
def serve_stylesheet():
    return server.send_static_file('style.css')
    
@server.route('/favicon.ico')
def favicon():
    return server.send_static_file('400x400SML-01.png')
    
@server.route('/download/<path:path>')
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)
    
app = dash.Dash('Clustering demo app', server=server, url_base_pathname='/', csrf_protect=False)
app.config['suppress_callback_exceptions']=True

app.css.append_css({
    'external_url': '/static/style.css'
})

app.title = 'Clustering demo dashboard'

data_df = get_data()
X_red = dim_reduce(data_df)

starting_plot = go.Figure(
    data = [
        go.Scatter(
            x = X_red[:,0],
            y = X_red[:,1],
            mode = 'markers',
            marker = dict(
                size = 2.5
            )
        )
    ],
    layout = go.Layout(
        xaxis = dict(
            title = 'x (reduced)'
        ),
        yaxis = dict(
            title = 'y (reduced)'
        ),
        margin = dict(l=30, b=30, t=0, r=0),
        hovermode='closest'
    )
)

selector = dcc.RadioItems(
    id='selector',
    options=[
        {'label': '1', 'value': '1'},
        {'label': '2', 'value': '2'},
        {'label': '3', 'value': '3'},
        {'label': '4', 'value': '4'}
    ],
    value='1'
)

app.layout = html.Div(
    id='app-container',
    children=[
        html.H1('Clustering dashboard'),
        html.Div(
            [html.Div([
                dcc.Markdown('Select the number of clusters:'),
                selector,
                html.Br(),
                html.Button('Compute', id='button')],
                className='three columns'
            ),
            html.Div(
                id='plot-container',
                children = [
                    dcc.Graph(
                        id='cluster-plot',
                        figure=starting_plot
                    )
                ],
                className='nine columns'
            )],
            className='row'
        )
    ]
)

@app.callback(
    Output('cluster-plot', 'figure'),
    [Input('button', 'n_clicks')],
    [State('selector', 'value')]
)
def compute_clusters(n_clicks, n_clusters):
    if n_clicks:
        n_clusters=int(n_clusters)
        clusters_df = clusterize(X_red, n_clusters)
        data = []
        for label in clusters_df['cluster'].unique():
            data.append(
                go.Scatter(
                    x = clusters_df[clusters_df['cluster']==label]['x_red'],
                    y = clusters_df[clusters_df['cluster']==label]['y_red'],
                    mode = 'markers',
                    marker = dict(
                        size = 2.5
                    ),
                    name = 'cluster '+str(label)
                )   
            )
        layout = go.Layout(
            xaxis = dict(
                title = 'x (reduced)'
            ),
            yaxis = dict(
                title = 'y (reduced)'
            ),
            margin = dict(l=30, b=30, t=0, r=0),
            hovermode='closest'
        )
        fig = go.Figure(data=data, layout=layout)
    
        return fig
    else:
        pass
        
if __name__ == '__main__':
    server.run(port=8888)
    
    print('''REMEMBER TO UPDATE THE CREDENTIAL FILE IF THE URL/KEY FOR THE API HAS CHANGED''')