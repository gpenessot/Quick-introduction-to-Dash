#Import des librairies
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output  
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd

os.chdir('C:/Users/h19656/Documents/Data Science/DataCamp/Instructor position/')
df = pd.read_csv('test.csv')
df.index = pd.DatetimeIndex(df['Date'])
#df.sort_index()
df.columns = [ 'index', 'Date', 'Manager', 'Gross Margin (€)', 'Cumumated Gross Margin (€)']
#print(df.head())


# Initialise the app 
app = dash.Dash(__name__) 

# Creates a list of dictionaries, which have the keys label and value. 
def get_options(list_manager): 
	dict_list = [] 
	for i in list_manager : 
		dict_list.append({'label': i, 'value': i}) 
	return dict_list 

@app.callback(Output('timeseries', 'figure'),
              [Input('selector', 'value')]) 
def update_timeseries(selected_dropdown_value):
  trace = []
  df_sub = df
  for manager in selected_dropdown_value:
    trace.append(
			go.Scatter(x=df_sub[df_sub['Manager'] == manager].index,
				  y=df_sub[df_sub['Manager'] == manager]['Cumumated Gross Margin (€)'],
				  mode='lines', 
				  opacity=0.7, 
				  name= manager, 
				  textposition='bottom center'))
  traces = [trace]
  data = [val for sublist in traces for val in sublist] 
  figure = {'data': data,
		        'layout': go.Layout(colorway=['#5E0DAC', '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'], 
	          template='plotly_dark', 
		        paper_bgcolor = 'rgba(0, 0, 0, 0)', 
		        plot_bgcolor = 'rgba(0, 0, 0, 0)', 
	 	        margin={'b': 15}, 
            hovermode='x', 
		        autosize=True, 
		        title={'text': 'Cumumated Gross Margin (€) - 2021', 
                   'font': {'color': 'white'}, 
                   'x': 0.5},
            xaxis={'range': [df_sub.index.min(), df_sub.index.max()]}, ), } 
  return figure 



# Define the app 
app.layout = html.Div(children=[
                      html.Div(className='row',
                               children=[
                                        html.Div(children = [
                                            html.H2('2021 Gross Margin'),
                                            html.P('Visualizing time series with Plotly'),
                                            html.P('Pick one or more Manager to visualize results'),
                                            html.Div(className='div-for-dropdown',
                                                      children = [ 
                                                      dcc.Dropdown(id='selector',
                                                              options=get_options(df['Manager'].unique()), 
                                                              multi=True, 
                                                              value=[df['Manager'].sort_values()[0]],
                                                              style={'backgroundColor': '#000000'},
                                                              className='selector') ], 
                                                              style={'color': '#FFFFFF'}) 
 
                                    ] 
                                    , className='four columns div-user-controls'),
                                  html.Div(children=[
                                    dcc.Graph(id='timeseries',
                                              config={'displayModeBar': False},
                                              animate=True,
                                              figure=px.line(df,
                                                  x='Date',
                                                  y='Cumumated Gross Margin (€)',
                                                  color='Manager',
                                                  template='plotly_dark').update_layout({
                                                  'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                                                  'paper_bgcolor' : 'rgba(0, 0, 0, 0)'
                                                  }) 
                                                ) 
                                              ], className='eight columns div-for-charts bg-grey')
                                  ])
                                ])
# Run the app 
if __name__ == '__main__':
    app.run_server(debug=True)
