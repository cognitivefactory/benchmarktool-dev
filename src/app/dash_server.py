from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import csv
import os
from ast import literal_eval

def get_dataset_for_labels():
    df = pd.read_csv('./src/tmp/test.csv')
    df2 = pd.DataFrame(columns=['p' , 'r' ,'f','label', 'model_name'])
    for index, row in df.iterrows():
        data = row["score_by_label"]
        data = literal_eval(data)
        for key in data:
            dico = data[key]
            dico["label"] = key
            dico["model_name"] = row["model_name"]
            df2 = df2.append(data[key], ignore_index=True)  
    return(df2)

def filter_dataset_for_models(model_list,df):
    df_models = pd.DataFrame(columns = df.columns.tolist())
    for model_name in model_list:
        df_tmp = df[df["model_name"].eq(model_name)]
        df_models = pd.concat([df_models, df_tmp], axis=0, sort=False)
    return df_models

def get_dataset_for_losses():
    df = pd.read_csv('./src/tmp/test.csv')
    df['losses'] = df['losses'].apply(literal_eval) 
    df = df.explode('losses')
    df = df.reset_index()
    return df



def create_Dash(server):
    filepath = './src/tmp/test.csv'
    if os.path.exists(filepath):
        os.remove(filepath)
    with open('./src/tmp/test.csv', mode='w') as csv_file:
        fieldnames = ['model_name', 'precision', 'recall', 'f_score','score_by_label','losses']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    app = Dash(__name__,server=server,routes_pathname_prefix='/dash/')
    df = pd.read_csv('./src/tmp/test.csv')
    opts = [{'label' : i, 'value' : i} for i in df["model_name"].tolist()]


    app.layout = html.Div([

                html.Label("Choose a model"),
                #dropdown
                dcc.Dropdown(id = "models_list"),
                #refresh
                dcc.Interval(
                    id='interval_component',
                    interval=1*1000, # in milliseconds
                    n_intervals=0),
                #score by label
                    dcc.Graph(id='score_by_label'),
                    dcc.Checklist(id = "models_checklist"),
                    dcc.Graph(id = 'scores'),
                    dcc.Graph(id = 'losses')
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'})


    @app.callback([Output('models_list', 'options'),
                Output('models_checklist', 'options')],
                [Input('interval_component', 'n_intervals')])
    def update_models(n):
        df = pd.read_csv('./src/tmp/test.csv')
        if(len(df)==0):
            raise PreventUpdate
        else:
            options = [{'label' : i, 'value' : i} for i in df["model_name"].tolist()]
            return options, options

    @app.callback(Output('score_by_label', 'figure'),
                [Input('models_list', 'value')])
    def update_score_by_label(model):
        if (model == None):
            raise PreventUpdate
        df_scores = get_dataset_for_labels()
        df_scores = filter_dataset_for_models([model],df_scores)
        if(df_scores['model_name'].count()==0):
            raise PreventUpdate
        else:
            print(df_scores)
            print('-------------------')
            print(df_scores["label"])
            print('---------------------')
            fig = px.bar(df_scores, x = "label", y = ['p', 'r', 'f'], barmode='group', title = "scores par label")
            fig.update_layout(transition_duration=500)
        return fig
    
    @app.callback([Output('scores', 'figure'),
                Output('losses', 'figure')],
                [Input('models_checklist', 'value')])
    def update_models_display(models):
        if (models == None):
            raise PreventUpdate
        if (models == []):
            return {}, {}
        
        df =  pd.read_csv('./src/tmp/test.csv')
        df = filter_dataset_for_models(models,df)
        score_fig = px.bar(df, x = "model_name", y = ['precision', 'recall', 'f_score'], barmode='group', title = "scores des modèles")
        df_losses = get_dataset_for_losses()
        df_losses = filter_dataset_for_models(models,df_losses)
        losses_fig = px.line(df_losses, y = "losses", title = "loss")
        return score_fig, losses_fig

    return app.server
