#!/usr/bin/env python
# coding: utf-8


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from dash import html, Dash, dcc
from dash.dependencies import Input, Output, State

# ! pip install -U dash_bootstrap_components

df = pd.read_csv(r'C:/Users/yao/vgsales.csv')
df.head()

df.isna().sum()

# In[5]:


df.isna().any()

# In[6]:


df[['Year', 'Publisher']].describe(include='all')

# In[7]:


df.Year = df.Year.fillna(df.Year.mean())
df.Year = df.Year.astype('int32')
df.Year

# In[8]:


df.Publisher = df.Publisher.fillna(df.Publisher.mode()[0])

# In[9]:




# In[10]:


top_10_generes = df.Genre.value_counts()
fig1 = px.bar(top_10_generes, title='Top 10 Video Game Genres', labels={'value': "Number of Games Genres",
                                                                        'index': "Name of the Genre"},
              template='plotly_dark', barmode='overlay', opacity=0.7)
fig1.update_traces(marker_color='red')
fig1.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0.3)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0.3)',
})
top_10_publishers = df.Publisher.value_counts().head(10)
fig2 = px.bar(top_10_publishers, title='Top 10 Video Game Pubishers', labels={'value': "Number of Games Publishing",
                                                                              'index': "Name of the Publisher"},
              template='plotly_dark', barmode='overlay', opacity=0.7)
fig2.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0.3)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0.3)',
})
top_10_platform = df.Platform.value_counts()
fig3 = px.bar(top_10_platform, title='Top Playing Platforms',
              labels={'value': "Counts", 'index': "Name of the Platform"},
              template='plotly_dark', barmode='overlay', opacity=0.8)
fig3.update_traces(marker_color='green')
fig3.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0.3)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0.3)',
})

# In[11]:


new_df = df.loc[(df['Name'] == 'Tetris')]
sales = new_df.loc[:, ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].transpose()
sales.rename(columns={0: "sales"}, inplace=True)
sales['game'] = sales.index
sales['value'] = sales.iloc[:, 0]

sales.head()
pie_chart = px.pie(sales, names='game', values='value', title='Tetris',
                   color_discrete_sequence=px.colors.sequential.RdBu)
pie_chart.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0.3)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0.3)',
})

top_sales = df.sort_values(by=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'], ascending=False).head(10)
dicts_name = {'NA_Sales': "North America Sales ( In Millions)", 'EU_Sales': "Europe Sales ( In Millions)",
              'JP_Sales': "Japan Sales ( In Millions)", 'Other_Sales': "Other Sales ( In Millions)", }

year_wise_sales = df.loc[:, ['Name', 'Year', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].groupby(
    by='Year').mean()
fig6 = px.line(year_wise_sales, x=year_wise_sales.index, y=[year_wise_sales['NA_Sales'], year_wise_sales['EU_Sales'],
                                                            year_wise_sales['JP_Sales'],
                                                            year_wise_sales['Other_Sales']],
               title='Average Sales (In Millions)',
               labels={'value': "Sales", 'index': "Year"}, template='plotly_dark')
fig6.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0.3)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0.7)',
})

# In[12]:


# scatter1= px.scatter(df, x='Year', y='Global_Sales', color='Genre', size='Rank', hover_data=['Name'], size_max=40)


# In[13]:

app = dash.Dash(title='Interactive Model Dashboard', external_stylesheets=[
    'https://codepen.io/chriddyp/pen/bWLwgP.css'])  # external_stylesheets=[external_stylesheets]
server = app.server

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.tiltle = 'Video Game Sales'
app.layout = html.Div([html.Br(),
                       html.B(
                           html.H1('Games Industry Sales Insights', style={'color': 'white', 'text-align': 'center', }),

                           style={
                               'background-image': 'url(https://media.istockphoto.com/vectors/retro-neon-background-with-80s-styled-laser-grid-and-stars-vector-id1140828326?k=20&m=1140828326&s=612x612&w=0&h=Lr8emBoEVyktilfc8USOINtfj3kM3qwNiwQzBFhZmi8=)'}),
                       html.Br(), html.Br(),

                       html.Div([dbc.Row(
                           [dbc.Col(dbc.Card(dbc.CardBody([html.H3("Top Genre "), html.H4("Action")]),
                                             style={"background-color": "red", 'width': '50%', 'height': '90%',
                                                    'display': 'inline-block', 'padding': '0 10'})),  # col
                            dbc.Col(dbc.Card(dbc.CardBody([html.H3("Top Publisher "), html.H4("Electronic Arts")]),
                                             style={"background-color": "blue", 'width': '50%', 'height': '90%',
                                                    'display': 'inline-block', 'padding': '0 10'})),  # col
                            dbc.Col(dbc.Card(dbc.CardBody([html.H3("Top Platform "), html.H4("DS")]),
                                             style={"background-color": "green", 'width': '50%', 'height': '90%',
                                                    'display': 'inline-block', 'padding': '0 10'}))],  # col

                       )
                       ]),

                       html.Div(dcc.Graph(id='fig1', figure=fig1),
                                style={'width': '30%', 'height': '35%', 'display': 'inline-block', 'padding': '0 10'}),
                       html.Div(dcc.Graph(id='fig2', figure=fig2),
                                style={'width': '40%', 'height': '35%', 'display': 'inline-block', 'padding': '0 '}),
                       html.Div(dcc.Graph(id='fig3', figure=fig3),
                                style={'width': '30%', 'height': '35%', 'display': 'inline-block', 'padding': '0'}),

                       # html.Div(dcc.Graph(id='scatter1',figure=scatter1)),
                       html.Br(), html.Br(),

                       html.Div(dcc.Graph(id='fig6', figure=fig6),
                                style={'width': '90%', 'height': '35%', 'display': 'inline-block', 'padding': '0 10'}),

                       html.Br(), html.Br(),

                       html.Div([html.B(html.Label(['Choose a game:'])), html.Br(), html.Br(),
                                 dcc.Dropdown(df['Name'], 'Super Mario Bros.', id='drop1', style={'color': 'black'}),
                                 dbc.Button("More info", id="help", style={'color': 'white'}),
                                 dbc.Tooltip("This chart shows sales percentges across regions for the game you select",
                                             target="help", style={'color': 'black', 'text-align': 'center'}),
                                 dcc.Graph(id='pie1', figure=pie_chart)]),

                       # html.Div(dcc.Slider(0,9,1, )),

                       html.Div([html.Br(), html.Div(id='output_data1'), html.Br(), html.Label(['Choose region:'],
                                                                                               style={
                                                                                                   'font-weight': 'bold',
                                                                                                   "text-align": "center"}),
                                 html.Br(),
                                 dcc.RadioItems(id='my_radio', options=[
                                     {'label': 'North America', 'value': 'NA_Sales'},
                                     {'label': 'Europe', 'value': 'EU_Sales'},
                                     {'label': 'Japan', 'value': 'JP_Sales'},
                                     {'label': 'Other', 'value': 'Other_Sales'}],
                                                value='NA_Sales',
                                                inline=True,
                                                style={'width': "100%", 'color': 'white', 'size': 10, "font-size": 20,
                                                       "padding": "30px"},
                                                labelStyle={
                                                    'display': 'inline-block',
                                                    'margin-right': '20px',
                                                    'font-weight': 500
                                                }),

                                 html.Br()]),

                       html.Div([dcc.Graph(id='our_graph1')]),

                       html.Div([html.Br(), html.Div(id='output_data'), html.Br(), html.Label(['Choose region:'],
                                                                                              style={
                                                                                                  'font-weight': 'bold',
                                                                                                  "text-align": "center"}),
                                 dcc.Dropdown(id='my_dropdown', options=[
                                     {'label': 'North America ', 'value': 'NA_Sales'},
                                     {'label': 'Europe ', 'value': 'EU_Sales'},
                                     {'label': 'Japan ', 'value': 'JP_Sales'},
                                     {'label': 'Other Sales', 'value': 'Other_Sales'}],
                                              optionHeight=35,
                                              value='NA_Sales',
                                              disabled=False,
                                              multi=False,
                                              searchable=True,
                                              clearable=True,
                                              style={'width': "100%", 'color': 'black'}),
                                 html.Br(), ]),

                       html.Div(dcc.Graph(id='our_graph')),

                       ], style={'color': 'white', 'text-align': 'center',
                                 'background-image': 'url(https://media.istockphoto.com/vectors/retro-neon-background-with-80s-styled-laser-grid-and-stars-vector-id1140828326?k=20&m=1140828326&s=612x612&w=0&h=Lr8emBoEVyktilfc8USOINtfj3kM3qwNiwQzBFhZmi8=)'})


@app.callback(
    Output('pie1', 'figure'),
    Input('drop1', 'value')

)
def funct(dropdownvalue):
    new_df = df.loc[(df['Name'] == dropdownvalue)]
    sales = new_df.loc[:, ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].transpose()
    sales.rename(columns={0: "sales"}, inplace=True)
    sales['game'] = sales.index
    sales['value'] = sales.iloc[:, 0]

    pie_chart = px.pie(sales, names='game', values='value', title=dropdownvalue,
                       color_discrete_sequence=px.colors.sequential.RdBu, )
    pie_chart.update_traces(textposition='inside', textinfo='percent+label')

    pie_chart.update_layout(
        font_color="white",
        title_font_color="white",
        legend_title_font_color="white"
    )
    pie_chart.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0.3)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0.7)',
    })

    return pie_chart


@app.callback(
    Output(component_id='our_graph1', component_property='figure'),
    [Input(component_id='my_radio', component_property='value')]
)
def build_graph(button_chosen):
    fig4 = px.scatter(df, x="Year", y="Global_Sales", color="Genre", size=button_chosen, hover_data=['Name'],
                      size_max=40,
                      title="Year Wise Global Video Game Sales by Genere",
                      labels={'x': 'Years', 'y': 'Global Sales In Millions'}, template='plotly_dark')

    fig4.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0.6)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig4


@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)
def build_graph(column_chosen):
    fig5 = px.sunburst(top_sales, path=['Genre', 'Publisher', 'Platform'], values=column_chosen, template='plotly_dark')
    for (key, title) in dicts_name.items():
        if (column_chosen == key):
            fig5.update_layout(title={'text': 'Top Selling by ' + title,
                                      'font': {'size': 28}, 'x': 0.5, 'xanchor': 'center'})
    fig5.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0.6)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0.6)',
    })
    return fig5


# In[ ]:


# In[ ]:


app.run_server()

# In[ ]:


# In[ ]:
