



import dash
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import dash_table


def create_kpi_card(title, value, color):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(title, className="card-title"),
                html.H2(value, className="card-text"),
            ],
            style={'textAlign': 'center'}
        ),
        color=color, inverse=True
    )


def agg_function(dataframe, columns_groupby, columns_to_agg, agg_method, sort_by = None, ascending = False):
    """
    This function aggregates specified columns of a dataframe based on a grouping column 
    and a specified aggregation method, then sorts the result.
    
    Parameters:
    - dataframe: The input DataFrame.
    - columns_for_agg: The column(s) to group by (string or list of strings).
    - columns_to_agg: The column(s) to aggregate (string or list of strings).
    - agg_method: The aggregation method (string or function).
    - sort_by: The column(s) to sort by after aggregation (string or list of strings, optional).
    - ascending: Sort ascending vs. descending (default is False).
    
    Returns:
    - agg_dataframe: The aggregated and sorted DataFrame.
    """
    agg_dataframe = round(dataframe.groupby(columns_groupby)[columns_to_agg].agg(agg_method).reset_index(),2)
    
    # Dynamically rename columns based on the aggregation method
    new_column_names = {}
    if isinstance(agg_method, list):
        for method in agg_method:
            new_column_names[(columns_to_agg, method)] = f"{method}_{columns_to_agg}"
    else:
        new_column_names[columns_to_agg] = f"{agg_method}_{columns_to_agg}"
    
    agg_dataframe.rename(columns=new_column_names, inplace=True)
    
    # if sort_by:
    #     if isinstance(agg_method, list):
    #         sort_column = new_column_names.get((columns_to_agg, sort_by), sort_by)
    #     else:
    #         sort_column = new_column_names.get(columns_to_agg, sort_by)
    #     agg_dataframe = agg_dataframe.sort_values(by=sort_column, ascending=ascending)
    
    return agg_dataframe


# top_products by selected variable
def top_n_products(dataframe, agg_variable, filter_variable=None, value=None, n=5):
    try:
        if filter_variable and value:
            df = dataframe[dataframe[filter_variable] == value]
        else:
            df = dataframe.copy()  # If no filter is provided, consider the entire dataframe

        top_products = df[agg_variable].value_counts().reset_index().sort_values(by='count', ascending=False)[:n]
        return top_products
    except KeyError as e:
        print(f"KeyError: {e}. Check if the column '{filter_variable}' exists in the DataFrame.")
        return None



def update_univarChart(fig):
    '''this function formats the graph'''
    fig.update_layout(height = 400, width = 550, 
                    showlegend = False, 
                    yaxis = {'visible':False},
                    xaxis_title = "",
                    yaxis_title = "",
                    xaxis_tickangle =-25,
                    title = dict(x = 0.40)),
    fig.update_traces(marker_color = 'LightSeaGreen')

    return fig


def sumInfrequentProduct(dataframe, n):

    ''' This function takes n (integer) and prints the total number and percentage of 
    rows where Product_ID appears less than or equal to  n times'''
    
    product_counts = dataframe['Product_ID'].value_counts() 
    single_occurance_products = product_counts[product_counts <= n].index
    filtered_data = dataframe[dataframe["Product_ID"].isin(single_occurance_products)]
    print(f' The total number of Product_ID appears less than or equal to {n} times is: {filtered_data.shape[0]}, which is {(filtered_data.shape[0]/data.shape[0])*100:.4f}% of the total rows.')


def create_bins(dataframe, column, bins, labels, col_to_name):

    ''' This function creates a column that has value provided in the labels argument. 
    It takes dataframe, column in which padas cut method be applied, bins, and label definition (in a list) as arguments
    
    '''
    
    bins = bins
    labels = labels
    dataframe[col_to_name] = pd.cut(data[column], bins = bins, labels = labels)
    return dataframe


def dash_table_format(data_list, agg_data, page_size):
    return dash_table.DataTable(
            data=data_list,
            columns=[{'name': col, 'id': col} for col in agg_data.columns],
            # cell_selectable=False,
            # sort_action='native',
            # filter_action='native',
            # Add pagination
            # page_action='native',
            page_current=0,
            style_cell={"textAlign": 'left'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_table={'maxWidth': '400px'}, 
            style_data_conditional=[
                {
                    'if': {'column_id': 'mean', 'filter_query': '{mean} > 4.2'},
                    'backgroundColor': '#20B2AA',
                    'color': 'white'
                },
                {
                    'if': {'column_id': 'mean', 'filter_query': '{mean} <= 4.2'},
                    'backgroundColor': '#00a0b9',
                    'color': 'white'
                },

                {
                    'if': {'column_id': 'mean', 'filter_query': '{mean} <= 4'},
                    'backgroundColor': '#8C2008',
                    'color': 'white'
                }
            ]
        )
 

def drop_down_style(margin):
    '''
    This function takes no argument but returns the style
    and rsponsive size for the dropdown used in dashboards'''
    style = {
        "width": "200px", 
        'font-size': "13px", 
        "margin": margin}


    
    return style


def component_text(margin):
    '''
       This function takes no argument but returns the style
        and rsponsive size for the text used in dashboards'''

    style= {'textAlign': 'left', 
            'font-size': '15px', 
            "color": 'SeaGreen', 
            "margin": margin, 
            'font-size': "15px"}

    return style
