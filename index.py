                                                                            # Name: Aashish Bansal
                                                                            # Roll No.: 101917110
                                                                            # Batch: CSE5


                                                                # Global Terrorism Dataset visualisation Dashboard

# I have created this dashboard in python using ploty dash library. This dashboard has three input Components(One range slider and two dropdown lists).
# Range slider is drop down list dependent. The drop down list is created in dash app using chain callback.
# So by selecting any region from the first drop down list, we can see that in second drop down country name list is updated.
# So if I select a region in first drop down list, I can see the list of countries for this region in second drop down list.
# Range slider is also connected to the dependent drop down list.
# By selecting year values, these year values are updated on the combination of line chart and bar chart and we can also see data for this selected period on pie chart
# The scatter map box is also depend on these two inputs. I have created hover effect on this scatter chart. It displays many hover information.
# I have added the css style sheet to make this dashboard responsive on any device.



# Importing libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pandas.core.frame import DataFrame
import plotly.graph_objs as go
import pandas as pd

# Loading the dataset
terr2 = pd.read_csv('globalterrorism.csv')

location1 = terr2[['country_txt', 'latitude', 'longitude']] # location details
list_locations = location1.set_index('country_txt')[['latitude', 'longitude']].T.to_dict('dict') # creating dictionary, key as country, value as latitude and longitude

# DataFrame with unique list of region
region = terr2['region_txt'].unique()

# Dash App created and name given
app = dash.Dash(__name__,assets_folder="CSS") # assets_folder = CSS which contains CSS files for styling the dashboard

# created dash app layout in HTML div
app.layout = html.Div([
    # First row having heading
    html.Div([
        html.Div([
            html.Div([
                html.H3('Global Terrorism Database', style = {"margin-bottom": "0px", 'color': 'white'}), # heading and styles given
                html.H5('1970 - 2017', style = {"margin-top": "0px", 'color': 'white'}), # heading and styles given

            ]),
        ], className = "six column", id = "title") # class and id given for styling using css

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}), # class and id given for styling using css

    # Second row
    # scatter map
    html.Div([
        html.Div([
            dcc.Graph(id = 'map_1', config = {'displayModeBar': 'hover'}), # given id, creating graph
        ], className = "create_container 12 columns"), # class given for styling using css
    ], className = "row flex-display"), # class given for styling using css

    # Third row
    html.Div([
        html.Div([
            html.P('Select Region:', className = 'fix_label', style = {'color': 'white'}), # title given to region dropdown list
            # DropDown list for regions
            dcc.Dropdown(id = 'w_countries', # given id
                         multi = False, # for selecting only one value
                         clearable = True, # Whether or not the dropdown is "clearable", that is, whether or not a small "x" appears on the right of the dropdown that removes the selected value
                         disabled = False, # dropdown is enabled, If True, this dropdown is disabled and the selection cannot be changed
                         style = {'display': True}, # Defines CSS styles which will override styles previously set
                         value = 'South Asia', # The default value of the input
                         placeholder = 'Select Countries', # default text shown when no option is selected
                         options = [{'label': c, 'value': c}
                                    for c in region], className = 'dcc_compon'), # used region dataframe created above


            html.P('Select Country:', className = 'fix_label', style = {'color': 'white'}), # title given to country dropdown list
            # DropDown list for countries in that region
            dcc.Dropdown(id = 'w_countries1', # given id
                         multi = False, # for selecting only one value
                         clearable = True, # Whether or not the dropdown is "clearable", that is, whether or not a small "x" appears on the right of the dropdown that removes the selected value
                         disabled = False, # dropdown is enabled, If True, this dropdown is disabled and the selection cannot be changed
                         style = {'display': True}, # Defines CSS styles which will override styles previously set
                         placeholder = 'Select Countries', # default text shown when no option is selected
                         options = [], className = 'dcc_compon'), # created empty list for options, so that when I select region in above drop down, I get countries corresponding to that region
            
            # Range slider created for year selection
            html.P('Select Year:', className = 'fix_label', style = {'color': 'white', 'margin-left': '1%'}), # title of range slider
            dcc.RangeSlider(id = 'select_years', # id of range slider
                            min = 1970, # minimum value of year
                            max = 2017, # maximum value of year
                            dots = False, # dots on slider set to false
                            value = [2010, 2017]), # default value

        ], className = "create_container three columns"), # class given for styling using css

        # Line and Bar chart
        html.Div([
            dcc.Graph(id = 'bar_line_1', config = {'displayModeBar': 'hover'}), # id given to bar and line chart combination
        ], className = "create_container six columns"), # class given for styling using css

        # Pie chart
        html.Div([
            dcc.Graph(id = 'pie', config = {'displayModeBar': 'hover'}), # id given to pie chart
        ], className = "create_container three columns"), # class given for styling using css

    ], className = "row flex-display"), # class given for styling using css

], id = "mainContainer", style = {"display": "flex", "flex-direction": "column"}) # id given for styling using css


# After selecting the region, to get the countries that region in second dropdown
@app.callback(
    Output('w_countries1', 'options'), # Output will be in empty options list created above in dropdown layout
    Input('w_countries', 'value')) # first drop down list and input is value
# function to get the countries in the list
def get_country_options(w_countries):
    terr3 = terr2[terr2['region_txt'] == w_countries] # filter region column with input id
    return [{'label': i, 'value': i} for i in terr3['country_txt'].unique()] # returned the unique list of countries in options list

# First value of the country in the list as default value
@app.callback(
    Output('w_countries1', 'value'), # output id of second drop down list and returned in value
    Input('w_countries1', 'options')) # input id given and options list of countries
def get_country_value(w_countries1): # used id as key argument
    return [k['value'] for k in w_countries1][0] # returned list of values and selected first row of the value list

# Dynamic disk scatter map box chart
# Create scatter map box chart
@app.callback(Output('map_1', 'figure'), # map_1 is id of scatter map and output is figure
              [Input('w_countries', 'value')], # region dropdown list as input
              [Input('w_countries1', 'value')], # country dropdown list as input
              [Input('select_years', 'value')]) # range slider as input
def update_graph(w_countries, w_countries1, select_years): # used above three id's as key argument
    # DataFrame creation
    terr3 = terr2.groupby(['region_txt', 'country_txt', 'provstate', 'city', 'iyear', 'latitude', 'longitude'])[['nkill', 'nwound']].sum().reset_index()
    terr4 = terr3[(terr3['region_txt'] == w_countries) & (terr3['country_txt'] == w_countries1) & (terr3['iyear'] >= select_years[0]) & (terr3['iyear'] <= select_years[1])]

    if w_countries1:
        zoom = 3
        zoom_lat = list_locations[w_countries1]['latitude']
        zoom_lon = list_locations[w_countries1]['longitude']


    return {
        # data information
        'data': [go.Scattermapbox(
            lon = terr4['longitude'],
            lat = terr4['latitude'],
            mode = 'markers',
            marker = go.scattermapbox.Marker(
                size = terr4['nwound'],
                color = terr4['nwound'],
                colorscale = 'hsv',
                showscale = False,
                sizemode = 'area'),

            # hover information
            hoverinfo = 'text',
            hovertext =
            '<b>Region</b>: ' + terr4['region_txt'].astype(str) + '<br>' +
            '<b>Country</b>: ' + terr4['country_txt'].astype(str) + '<br>' +
            '<b>Province/State</b>: ' + terr4['provstate'].astype(str) + '<br>' +
            '<b>City</b>: ' + terr4['city'].astype(str) + '<br>' +
            '<b>Longitude</b>: ' + terr4['longitude'].astype(str) + '<br>' +
            '<b>Latitude</b>: ' + terr4['latitude'].astype(str) + '<br>' +
            '<b>Killed</b>: ' + [f'{x:,.0f}' for x in terr4['nkill']] + '<br>' +
            '<b>Wounded</b>: ' + [f'{x:,.0f}' for x in terr4['nwound']] + '<br>' +
            '<b>Year</b>: ' + terr4['iyear'].astype(str) + '<br>'

        )],

        # layout information
        'layout': go.Layout(
            margin = {"r": 0, "t": 0, "l": 0, "b": 0},
            hovermode = 'closest',
            mapbox = dict(
                accesstoken = 'pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',  # Use mapbox token here
                center = go.layout.mapbox.Center(lat = zoom_lat, lon = zoom_lon),
                style = 'dark',
                zoom = zoom
            ),
            autosize = True,

        )

    }

# Create combination of bar and line  chart (show number of attack and death)
@app.callback(Output('bar_line_1', 'figure'), # bar_line_1 is id of combination of line and bar chart and output is figure
              [Input('w_countries', 'value')],  # region dropdown list as input
              [Input('w_countries1', 'value')], # country dropdown list as input
              [Input('select_years', 'value')]) # range slider as input
def update_graph(w_countries, w_countries1, select_years): # used above three id's as key argument
    # Data for line and bar
    # DataFrame creation
    terr5 = terr2.groupby(['region_txt', 'country_txt', 'iyear'])['nkill'].sum().reset_index() # used groupby to get specific column
    terr6 = terr5[(terr5['region_txt'] == w_countries) & (terr5['country_txt'] == w_countries1) & (terr5['iyear'] >= select_years[0]) & (terr5['iyear'] <= select_years[1])] # filtered the data using above three id's
    terr7 = terr2.groupby(['region_txt', 'country_txt', 'iyear'])[['attacktype1', 'nwound']].sum().reset_index() # used groupby to get specific column
    terr8 = terr7[(terr7['region_txt'] == w_countries) & (terr7['country_txt'] == w_countries1) & (terr7['iyear'] >= select_years[0]) & (terr7['iyear'] <= select_years[1])] # filtered the data using above three id's

    return {
        # properties for combination chart
        'data': [go.Scatter(x = terr6['iyear'],
                            y = terr6['nkill'],
                            mode = 'lines+markers',
                            name = 'Death',
                            line = dict(shape = "spline", smoothing = 1.3, width = 3, color = '#FF00FF'),
                            marker = dict(size = 10, symbol = 'circle', color = 'white',
                                          line = dict(color = '#FF00FF', width = 2)
                                          ),
                            # hover information
                            hoverinfo = 'text',
                            hovertext =
                            '<b>Region</b>: ' + terr6['region_txt'].astype(str) + '<br>' +
                            '<b>Country</b>: ' + terr6['country_txt'].astype(str) + '<br>' +
                            '<b>Year</b>: ' + terr6['iyear'].astype(str) + '<br>' +
                            '<b>Death</b>: ' + [f'{x:,.0f}' for x in terr6['nkill']] + '<br>'

                            ),
                # information for bar and line chart
                 go.Bar(
                     x = terr8['iyear'],
                     y = terr8['attacktype1'],
                     text = terr8['attacktype1'],
                     texttemplate = '%{text:.2s}',
                     textposition = 'auto',
                     name = 'Attack',

                     marker = dict(color = 'orange'),

                    # hover information
                     hoverinfo = 'text',
                     hovertext =
                     '<b>Region</b>: ' + terr8['region_txt'].astype(str) + '<br>' +
                     '<b>Country</b>: ' + terr8['country_txt'].astype(str) + '<br>' +
                     '<b>Year</b>: ' + terr8['iyear'].astype(str) + '<br>' +
                     '<b>Attack</b>: ' + [f'{x:,.0f}' for x in terr8['attacktype1']] + '<br>'
                 ),

                 go.Bar(x = terr8['iyear'],
                        y = terr8['nwound'],
                        text = terr8['nwound'],
                        texttemplate = '%{text:.2s}',
                        textposition = 'auto',
                        textfont = dict(
                            color = 'white'
                        ),
                        name = 'Wounded',

                        marker = dict(color = '#9C0C38'),

                        # hover information
                        hoverinfo = 'text',
                        hovertext =
                        '<b>Region</b>: ' + terr8['region_txt'].astype(str) + '<br>' +
                        '<b>Country</b>: ' + terr8['country_txt'].astype(str) + '<br>' +
                        '<b>Year</b>: ' + terr8['iyear'].astype(str) + '<br>' +
                        '<b>Wounded</b>: ' + [f'{x:,.0f}' for x in terr8['nwound']] + '<br>'
                        )],

        # layout information
        'layout': go.Layout(
            barmode = 'stack',
            plot_bgcolor = '#010915',
            paper_bgcolor = '#010915',
            title = {
                'text': 'Attack and Death : ' + (w_countries1) + '  ' + '<br>' + ' - '.join(
                    [str(y) for y in select_years]) + '</br>',

                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                'color': 'white',
                'size': 20},

            hovermode = 'x',

            xaxis = dict(title = '<b>Year</b>',
                         tick0 = 0,
                         dtick = 1,
                         color = 'white',
                         showline = True,
                         showgrid = True,
                         showticklabels = True,
                         linecolor = 'white',
                         linewidth = 2,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white'
                         )

                         ),

            yaxis = dict(title = '<b>Attack and Death</b>',
                         color = 'white',
                         showline = True,
                         showgrid = True,
                         showticklabels = True,
                         linecolor = 'white',
                         linewidth = 2,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white'
                         )

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#010915',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

# Creating pie chart
@app.callback(Output('pie', 'figure'), # pie is id of pie chart and output is figure
              [Input('w_countries', 'value')], # region dropdown list as input
              [Input('w_countries1', 'value')], # country dropdown list as input
              [Input('select_years', 'value')]) # range slider as input
def display_content(w_countries, w_countries1, select_years): # used above three id's as key argument
    # creating Dataframe
    terr9 = terr2.groupby(['region_txt', 'country_txt', 'iyear'])[
        ['nkill', 'nwound', 'attacktype1']].sum().reset_index()
    death = terr9[(terr9['region_txt'] == w_countries) & (terr9['country_txt'] == w_countries1) & (terr9['iyear'] >= select_years[0]) & (terr9['iyear'] <= select_years[1])]['nkill'].sum()
    wound = terr9[(terr9['region_txt'] == w_countries) & (terr9['country_txt'] == w_countries1) & (terr9['iyear'] >= select_years[0]) & (terr9['iyear'] <= select_years[1])]['nwound'].sum()
    attack = terr9[(terr9['region_txt'] == w_countries) & (terr9['country_txt'] == w_countries1) & (terr9['iyear'] >= select_years[0]) & (terr9['iyear'] <= select_years[1])]['attacktype1'].sum()
    colors = ['#FF00FF', '#9C0C38', 'orange']

    # pie chart information
    return {
        'data': [go.Pie(labels = ['Total Death', 'Total Wounded', 'Total Attack'],
                        values = [death, wound, attack],
                        marker = dict(colors = colors),
                        hoverinfo = 'label+value+percent',
                        textinfo = 'label+value',
                        textfont = dict(size = 13)
                        )],

        # Layout for pie chart
        'layout': go.Layout(
            plot_bgcolor = '#010915',
            paper_bgcolor = '#010915',
            hovermode = 'closest',
            title = {
                'text': 'Total Casualties : ' + (w_countries1) + '  ' + '<br>' + ' - '.join(
                    [str(y) for y in select_years]) + '</br>',

                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                'color': 'white',
                'size': 20},
            legend = {
                'orientation': 'h',
                'bgcolor': '#010915',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white')
        ),

    }



# main
if __name__ == '__main__':
    app.run_server(debug = True)
