# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
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
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'}
                                    ] + [
                                        {'label': site, 'value': site}
                                        for site in spacex_df['Launch Site'].unique()
                                    ],
                                    value='ALL',  # Default dropdown value
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,                 # Slider minimum value (Kg)
                                    max=10000,             # Slider maximum value (Kg)
                                    step=1000,             # Slider step size (Kg)
                                    value=[min_payload, max_payload],  # Current selected range
                                    marks={i: str(i) for i in range(0, 10001, 2500)}
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Use all data and show total successful launches by site
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        # Count success (1) and failure (0)
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failed Launches for site {entered_site}'
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_plot(entered_site, payload_range):
    # Get payload range
    low, high = payload_range

    # Filter dataframe based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':
        # Scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Outcome for All Sites'
        )
        return fig
    else:
        # Filter data for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]

        # Scatter plot for selected site
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Launch Outcome for site {entered_site}'
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run()


# Finding Insights Visually

# 1. Which site has the largest successful launches? 
#    The site that has the largest successful launches is KSC LC-39A, with 41.7% of all successfull launches
#    happening at this site.
 
# 2. Which site has the highest launch success rate?
#    The site with the highest launch success rate is also KSC LC-39A, with a high 76.9% of launches from this
#    site succeding in their outcome.

# 3. Which payload range(s) has the highest launch success rate?
#    There does not seem to be any payload range that has a higher launch success rate. Ranges that seem to have
#    good success rate have similar values in the negative side.

# 4. Which payload range(s) has the lowest launch success rate?
#    The payload range that has the lowest launch success rate comes for payload values of over 5500 kgs.

# 5. Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
#    B5 seems to have the highest success rate, but it may not be a good version to consider as it seems to have only had
#    one launch with one exact payload. The following version in terms of success rate would be FT.