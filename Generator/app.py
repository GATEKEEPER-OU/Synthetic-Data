# This runs the Data Generator. We only need the lines
#
# from dataGenModel import DataGenModel
# data_generator = DataGenModel(<coding>, maxTimings = <maxTimings>, eventTemperature = <temperature>)
# results_file = data_generator.generate_single_user()
#
# The rest of the code is UX. The code can be adapted to generate a single timing for demo purposes.
# The result file can be displayed to the screen. However the goal of this exercise is to get something deployed.
# We can play with the UX later.

from dataGenModel import DataGenModel

# The imports below are needed for a front-end. 
# The alternative is to accept parameters from the command line or from a file
from dash import Dash, dcc, html, Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
from config import codingFile

# Needed for drop-down list
codingDF = pd.read_csv(codingFile)
coding = codingDF['coding'].values.tolist()
display = codingDF['display'].values.tolist()

# coding = '41950-7'
# maxTimings = 100
# temperature = 0.1

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

code_list = [i + " - " + j for i, j in zip(coding, display)]

form = dbc.Form([
    dbc.Row(
        html.Div([dbc.Label("Default Coding"),
         dcc.Dropdown(code_list, code_list[0], id="coding")])
    ),
    dbc.Row(
        html.Div([dbc.Label("Maximum number of events (1-100)"),
         dbc.Input(type="number", min=1, max=100, id="times")])
    ),
    dbc.Row(
        html.Div([dbc.Label("Events Temperature (0-1)", width="auto"),
         dbc.Input(type="number", min=0.0, max=1.0, step=0.1, id="temperature")])
    ),
    dbc.Row(
        html.Div([html.P(" "), dbc.Button("Submit", color="primary", n_clicks=0, id="generate-btn")])
    )
])
    
app.layout = html.Div([
    dbc.Row(html.H2('Samsung GateKeeper DeepLearning Demo - Version 2')),
    form,
    dbc.Row([   html.P(" "),
                html.Hr( ),
                html.Div(id='dd-output-container')
            ]
    )
])

@app.callback(Output('dd-output-container', 'children'),
              Input('generate-btn', 'n_clicks'),
              State('coding', 'value'),
              State('times', 'value'),
              State('temperature', 'value'))
def update_output(n_clicks, coding, timings, temperature):
    if n_clicks == 0:
        return ""
    
    # This generates a file of results.
    start_coding = coding.split()[0]
    max_timings = timings

    data_generator = DataGenModel(start_coding, maxTimings = max_timings, eventTemperature = temperature)
    results_file = data_generator.generate_single_user()
    print(results_file)

    text = results_file + ' has been generated and is awaitng evaluation'
    return text

if __name__ == '__main__':
    app.run_server(debug=True)