# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{"value": "ALL", "label": "All sites"}] + [{"value": element, "label": element} for element in spacex_df["Launch Site"].unique()],
                                            value='ALL',
                                            placeholder="place holder here",
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        2000: "2000",
                                                        4000: "4000",
                                                        6000: "6000",
                                                        8000: "8000",
                                                        10000: "10000",
                                                        },
                                                value=[4000, 6000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, 
        names='Launch Site', 
        title='Total success launches by site')
        return fig
    else:
        fig = px.pie(spacex_df[spacex_df["Launch Site"] == entered_site], 
        names='class', 
        title='Total success launches by site')
        return fig 
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_plot(entered_site, slider_values):
    
    if entered_site == "ALL":
        fig = px.scatter(spacex_df[(slider_values[0]<= spacex_df["Payload Mass (kg)"]) & (spacex_df["Payload Mass (kg)"] <= slider_values[1])], x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig
    else:
        fig = px.scatter(spacex_df[(spacex_df["Launch Site"] == entered_site) & (slider_values[0]<= spacex_df["Payload Mass (kg)"]) & (spacex_df["Payload Mass (kg)"] <= slider_values[1])], x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
