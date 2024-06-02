# import re
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_table
from dash_table import DataTable, FormatTemplate
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import my_app_module as mam
from datetime import datetime

# Load data
data1 = pd.read_csv('app_data.csv')
data1['Product_ID'] = data1['Product_ID'].astype(str)
data1 = data1[["Product_ID", "Product type", 'Age group', 'Frequency level', 'Rating']]
data1.dropna(inplace=True)
problems = pd.read_csv('problems.csv')
complements = pd.read_csv('complements.csv')

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server
app.layout = dbc.Container(
    fluid=False,
    style = {'border': '2px solid #ccc', 'border-radius': '5px'},
    children=[
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                    html.Div(
                        'Product Review Analysis',
                        style={'font-family': 'Montserrat',
                        'font-size': 30, 
                        'textAlign': 'left', 
                        'color': 'LightSeaGreen', 
                        'margin': '10px 0px 0px 0px', 
                        'margin-bottom': '0px'
                        }
                    ),
                    html.H5('By Deyoz Rayamajhi', 
                                style={'textAlign': 'left', 
                                "color": 'Purple',
                                'font-size': 12
                                }
                            
                            )
                    ], xs=9, sm=9, md=9, lg=9, xl=9, xxl=9
                ),

                dbc.Col(
                    html.Div( id = 'current_datetime',
                    style={'font-family': 'Montserrat',
                            'font-size': 20, 
                            'textAlign': 'left', 
                            'color': 'LightSeaGreen', 
                            'margin': '30px 0px 0px 0px', 
                            'margin-bottom': '0px'
                            }
                        )
                ),
                dbc.Col(
                    html.Img(
                        src='assets/insight.png',
                        style={'height': '45px', 'width': '100%', 'margin': '20px 0px 0px -20px'}
                    ),
                    xs=6, sm=6, md=3, lg=3, xl=1, xxl=1
                )
            ]
        ),
        html.Br(),
        html.Hr(style={"color": 'grey', 'borderWidth': '2px', 'margin': '0px 0px 0px 0px'}),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(id='reviews_card', width=2),
                dbc.Col(id='products_card', width=2),
                dbc.Col(id='rating_card', width=2),
                dbc.Col(id='5_stars_card', width=2),
                dbc.Col(id='1_stars_card', width=2)
            ], style = {"margin": "0px 0px 0px 200px"}
        ),
        dcc.Interval(id='interval-component', interval=600000, n_intervals=0),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    
                        # html.H4(
                        #     'Select Variable ',
                        #     style={'textAlign': 'left', "color": 'SeaGreen', "margin": '-35px 0px 0px 135px', 'font-size': "15px"}
                        # ),
                        dcc.Dropdown(
                            id='dropdown1',
                            options=[{"label": i, 'value': i} for i in ["Product type", 'Age group', 'Frequency level']],
                            value='Product type',
                            style={"margin": "-10px 0px 5px 65px", 
                                    "width": "150px", 
                                    'font-size': "13px"
                                    }
                        )
                    
                ),

                dbc.Col(
                    html.H4(
                            'Select Variable ',
                            style={'textAlign': 'left', 
                                "color": 'SeaGreen', 
                                "margin": '-0px 0px 0px -45px', 
                                'font-size': "15px"
                                }
                        ),

                ),
                dbc.Col(
                    
                        # html.H4(
                        #     'Select values ',
                        #     style={'textAlign': 'left', 'font-size': '15px', "color": 'SeaGreen', "margin": '-35px 0px 0px 138px', 'font-size': "15px"}
                        # ),
                        dcc.Dropdown(
                            id='dropdown2',
                            value=None,
                            style={"margin": "-15px 0px 5px 65px", 
                                    "width": "150px", 'font-size': "12px"}
                        )
                    
                ),
                dbc.Col(
                    html.H4(
                            'Select value ',
                            style={'textAlign': 'left', 
                                    'font-size': '15px', 
                                    "color": 'SeaGreen', 
                                    "margin": '-5px 0px 0px -45px', 
                                    'font-size': "15px"}
                        ),      
                )
                # dbc.Col(
                #     [
                #         # Additional controls can be added here if needed
                #     ]
                # )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='barchart1', config={'responsive': True},
                        style={"margin": "-2px 0px 0px 60px", 
                                "width": "150px"}),
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='barchart_2', config={'responsive': True},
                        style={"margin": "-10px 0px 0px 60px", 
                                "width": "150px"}),
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H6(""),
                    # style={'textAlign': 'left', "margin": '0px 0px 0px 110px'})
                ),
                # html.Br(),
                # html.Br(),
                dbc.Col(
                    dbc.Button(
                        "Positive Review",
                        id="positive-reviews-button",
                        className="me-2",
                        outline=True,
                        size = 'sm',
                        style={'backgroundColor': 'LightSeaGreen', 'color': 'white',
                        "margin": "-5px 170px 0px 10px"}),
                         width='auto'
                
                )
                ,
                dbc.Col(
                    dbc.Button(
                        "Negative Review",
                        id="negative-reviews-button",
                        outline=True,
                        size = 'sm',
                        style={'backgroundColor': '#8C2008', 'color': 'white',
                        "margin": "-5px 170px 0px 10px"}
                    ),
                    width='auto'
                )
            ],
            justify='left'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Col(
                            html.H6("Average Ratings by select variable",
                                style={'textAlign': 'left', 
                                "margin": '0px 0px 0px 110px'})
                            ),
                            html.Br(),
                            html.Br(),
                            html.Div(id='table_container', style={"margin": '0px 0px 0px 125px'}
                                                                
                                )
                    
                    ]       
                ),

                dbc.Col(
                    dcc.Graph(id = 'doughnut_chart', config = {'responsive': True},
                    style={"margin": "2px 0px 0px 120px", 
                                "width": "500px"
                            }
                        )

                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('reviews_card', 'children'),
        Output('products_card', 'children'),
        Output('rating_card', 'children'),
        Output('5_stars_card', 'children'),
        Output('1_stars_card', 'children')
    ],
    [Input('interval-component', 'n_intervals')]
)
def update_cards(n):
    try:
        total_products = data1.shape[0]
        unique_products = data1['Product_ID'].nunique()
        avg_rating = round(data1['Rating'].mean(), 3)
        total_4plus_stars = data1[data1['Rating'] >= 4]['Rating'].count()
        total_3less_stars = data1[data1['Rating'] <= 3]['Rating'].count()

        return (
            mam.create_kpi_card('# Reviews', total_products, '#00a0b9'),
            mam.create_kpi_card('# Products', unique_products, '#00a0b9'),
            mam.create_kpi_card('Avg Rating', avg_rating, '#00a0b9'),
            mam.create_kpi_card('# 4+ Stars', total_4plus_stars, 'LightSeaGreen'),
            mam.create_kpi_card('# 3- Stars', total_3less_stars, '#8C2008')
        )
    except Exception as e:
        print(f"Error in update_cards callback: {e}")
    

@app.callback(
    Output('dropdown2', 'options'),
    Output('dropdown2', 'value'),
    [Input('dropdown1', 'value')]
)
def update_dynamic_dropdown(selected_variable):
    if selected_variable:
        options = [{'label': i, 'value': i} for i in data1[selected_variable].unique()]
        value = options[0]['value'] if options else None

        return options, value
    return [], None

@app.callback(
    Output('barchart1', 'figure'),
    [Input('dropdown1', 'value')]
)
def get_barchart1(menu):
    if menu:
        agg_data = mam.agg_function(data1, menu, 'Rating', ['count'])
        fig = px.bar(
            agg_data,
            x=menu,
            y='count',
            pattern_shape_sequence=[],
            title=f'Distribution of Reviews by {menu}',
            text_auto = True
        )
        mam.update_univarChart(fig)
        return fig
    return {}

@app.callback(
    Output('barchart_2', 'figure'),
    [Input('dropdown1', 'value'),
     Input('dropdown2', 'value')]
)
def get_barchart2(menu, value):
    if menu and value:
        filtered_data = data1[data1[menu] == value]
        agg_data = mam.top_n_products(filtered_data, 'Product_ID', filter_variable=menu, value=value, n=10)
        fig = px.bar(
            agg_data,
            x='Product_ID',
            y='count',
            pattern_shape_sequence=[],
            title=f'Top 10 products by {menu} and {value}',
            text_auto = True
        )
        mam.update_univarChart(fig)
        return fig
    return {}

@app.callback(
    Output('table_container', 'children'),
    [Input('dropdown1', 'value')]
)
def update_table(value):
    if not value:
        value = 'Product type'  # Assign a default value if 'value' is empty
    agg_data = mam.agg_function(data1, value, 'Rating', ['mean'])
    data_list = []
    for i in range(len(agg_data)):
        row = {col: agg_data[col][i] for col in agg_data.columns}
        data_list.append(row)
    table = mam.dash_table_format(data_list, agg_data, page_size=7
    
    )

    return table

@app.callback(
    Output("current_datetime", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_time(n):
    current_time = datetime.now().strftime("%B %d %y")
    return f"Date: {current_time}"


@app.callback(
    Output('doughnut_chart', 'figure'),
    [Input("positive-reviews-button", 'n_clicks'),
     Input("negative-reviews-button", 'n_clicks')],
    [State("positive-reviews-button", 'n_clicks'),
     State("negative-reviews-button", 'n_clicks')]
)
def get_doughnut_chart(pos_clicks, neg_clicks, pos_state, neg_state):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'positive-reviews-button'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "positive-reviews-button":
        complement_pie = px.pie(
            complements,
            values='proportion',
            names='label',
            hole=0.6,
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )

        # Update the layout
        complement_pie.update_layout(
            width=500,
            height=400,
            # title='Complement from all Positive Reviews',
            annotations=[dict(text='Complements', x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        return complement_pie

    elif button_id == "negative-reviews-button":
        problems_pie = px.pie(
            problems,
            values='proportion',
            names='label',
            hole=0.6,
            color_discrete_sequence=px.colors.sequential.solar
        )

        # Update the layout
        problems_pie.update_layout(
            width=500,
            height=400,
            # title='Problems with Dresses and Tops<br><sup> Negative reviews of 21-50 (Age group)',
            annotations=[dict(text='Problems', x=0.5, y=0.5, font_size=14, showarrow=False)]
        )

        return problems_pie

    else:
        # Default to show problems pie chart
        problems_pie = px.pie(
            problems,
            values='proportion',
            names='label',
            hole=0.6,
            color_discrete_sequence=px.colors.sequential.solar
        )

        # Update the layout
        problems_pie.update_layout(
            width=500,
            height=400,
            # title='Problems with Dress and Top<br><sup> Negative reviews of 21-50 (Age group)',
            annotations=[dict(text='Problems', x=0.5, y=0.5, font_size=14, showarrow=False)]
        )

        return problems_pie

if __name__ == "__main__":
    app.run_server(debug=True)


