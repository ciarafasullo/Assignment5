# %% [markdown]
# Ciara Fasullo
# evz5pv
# DS 4003
# Assignment 5: Callbacks

# %%
#import necessary modules
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# %%
#load the dataset
df = pd.read_csv('gdp_pcap.csv')
df

# %%
#reshape data to a tidy format
df = pd.melt(df, id_vars=['country'], var_name='year', value_name='gdpPercap')
df['year'] = df['year'].astype(int)  # convert 'year' column to integer
df

# %%
#initialize the dash app
app = dash.Dash(__name__)
#connect the server for Render
server = app.server

# %%
#define inline stylesheet
styles = {
    'body': {
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f0f0f0',  #light gray
        'margin': 0,
        'padding': '20px'
    },
    'title': {
        'color': '#444',  #dark gray
        'fontSize': '24px',
        'textAlign': 'center',
        'marginBottom': '20px'
    },
    'paragraph': {
        'color': '#666',  #medium gray
        'fontSize': '16px',
        'textAlign': 'center'
    },
    'dropdown': {
        'width': '100%',
        'marginBottom': '20px',
        'backgroundColor': '#e6e6e6',  #light gray
        'borderRadius': '5px'
    },
    'slider-container': {
        'width': '100%',
        'marginBottom': '20px'
    },
    'slider': {
        'width': '100%',
    },
    'graph': {
        'width': '100%',
        'height': '400px',
        'border': '1px solid #ccc',  #light gray
        'borderRadius': '5px',
        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
        'backgroundColor': '#f5f5f5'  #off-white
    }
}

# %%
#define app layout
app.layout = html.Div([
    #add a title at the top of the page
    html.H1("Gapminder GDP per Capita Insights", style=styles['title']),  #use inline styles
    #add a description of the data and app
    html.P("The gapminder dataset provides data on GDP per capita trends of each country since 1800."
           "Use this app to explore the trends of different countries using a variety of interactive features."
           "You may look at countries individually to compare its change in per capita GDP over time."
           "You may also select multiple countries to compare them with one another at various points in history.",
           style=styles['paragraph']),  #use inline styles
    html.Div([
        #dropdown for selecting countries
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['country'].unique()],
            multi=True,
            value=['United States'],  #default selection
            style=styles['dropdown']  #use inline styles
        ),
        #slider container
        html.Div([
            dcc.RangeSlider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                marks={str(year): str(year) if year % 50 == 0 else '' for year in df['year'].unique()},  # Display every 50th year
                value=[df['year'].min(), df['year'].max()],  #default selection converted to integers
                className="slider"  #add a class name for styling
            ),
        ], style=styles['slider-container']),  #apply styles to the container
    ]),
    #graph for displaying GDP data
    dcc.Graph(id='gdp-graph', style=styles['graph'])  #use inline styles
])

# %%
#define callback functions
@app.callback(
    Output('gdp-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_countries, selected_years):
    #convert selected_years to integers
    selected_years = [int(year) for year in selected_years]
    #filter the dataframe based on selected years
    filtered_df = df[(df['country'].isin(selected_countries)) & 
                     (df['year'].astype(int) >= selected_years[0]) & 
                     (df['year'].astype(int) <= selected_years[1])]
      
    traces = []
    for country in selected_countries:
        country_df = filtered_df[filtered_df['country'] == country]
        
        traces.append({'x': country_df['year'], 
                       'y': country_df['gdpPercap'], 
                       'mode': 'lines',
                       'name': country}) 

    return {
        'data': traces,
        'layout': {
            'title': 'GDP Per Capita Over Years',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'GDP Per Capita'}
         }
    }


# %%
#run the app
if __name__ == '__main__':
    app.run_server(debug=True)


