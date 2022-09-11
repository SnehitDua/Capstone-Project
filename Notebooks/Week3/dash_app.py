# Import required libraries
import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('./Week3/spacex_launch_dash.csv')
spacex_df['Outcome'] = ['Success' if i == 1 else 'Fail' for i in spacex_df['class']]
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children= [
        html.H1(
            'SpaceX Launch Records Dashboard',
            style= {
                'textAlign': 'center', 
                'color': '#503D36', 
                'font-size': 40
            }
        ),
        
        html.P('Select Launch Site: '),

        dcc.Dropdown(
            id= 'site-dropdown',
            options= [
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
            ],
            value= 'ALL',
            # placeholder= 'Select Launch Site: ',
            searchable= True
        ),

        html.Br(),

        html.Div(
            dcc.Graph(id= 'success-pie-chart')
        ),

        html.Br(),

        html.P('Payload Range (Kg): '),

        dcc.RangeSlider(
            id= 'payload-slider',
            min= 0,
            max= 10000,
            step= 1000,
            # marks= {
            #     0: '0', 
            #     100: '100'
            # },
            value= [min_payload, max_payload]
        ),

        html.Div(
            dcc.Graph(id= 'success-payload-scatter-chart')
        )
    ]
)

# Function decorator to specify function input and output
@app.callback(
    Output(
        component_id= 'success-pie-chart',
        component_property= 'figure'
    ),
    Input(
        component_id= 'site-dropdown',
        component_property= 'value'
    )
)
def get_pie_chart(entered_site):

    filtered_df = spacex_df[['Launch Site', 'class', 'Outcome']]

    if entered_site == 'ALL':
        fig = px.pie(filtered_df[filtered_df['class'] == 1], values= 'class', names= 'Launch Site', title= 'Total Success Launches By Site', labels= {'class': 'Successful Lauches'})
        fig.update_layout(legend= {'title': 'Launch Site'})
        return fig
    else:
        fig = px.pie(filtered_df[filtered_df['Launch Site'] == entered_site], names= 'Outcome', title= f'Total Success Launches For Site {entered_site}')
        fig.update_layout(legend= {'title': 'Outcome'})
        return fig

# Function decorator to specify function input and output
@app.callback(
    Output(
        component_id= 'success-payload-scatter-chart',
        component_property= 'figure'
    ),
    [
        Input(
            component_id= 'site-dropdown',
            component_property= 'value'
        ),
        Input(
            component_id= 'payload-slider',
            component_property= 'value'
        )
    ]
)
def get_scatter_chart(entered_site, entered_payload):

    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]

    if entered_site == 'ALL':
        fig = px.scatter(x= 'Payload Mass (kg)', y= 'class', color= 'Booster Version Category', data_frame= filtered_df)
        return fig
    else:
        fig = px.scatter(x= 'Payload Mass (kg)', y= 'class', color= 'Booster Version Category', data_frame= filtered_df[filtered_df['Launch Site'] == entered_site])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()