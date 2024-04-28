import pandas as pd
import numpy as np
import plotly.express as px

data_dir = "./data/skylab_instagram_datathon_dataset.csv"

def load_dataset():
    df = pd.read_csv(data_dir, delimiter=";")
    df.rename(columns={'business_entity_doing_business_as_name': 'brand', 'legal_entity_name': 'company', 
                    'ultimate_parent_legal_entity_name': 'parent_company'}, inplace=True)
    columns = df.columns
        
    df_without_dates = df.drop(['period', 'period_end_date'], axis=1)
    unique_values = {col: df_without_dates[col].unique() for col in df_without_dates.columns}
    return df   

def groupby_hierarchy(df):
    # Create different dataframes groupby and aggrete compset adn compset_group
    aggregated_df_by_brand = df.groupby('brand').agg({
        'compset_group': lambda x: set(x),
        'compset': lambda x: set(x)
    }).reset_index()

    aggregated_df_by_company = df.groupby('company').agg({
        'compset': lambda x: set(x),
        'compset_group': lambda x: set(x),
        'brand': lambda x: set(x)
    }).reset_index()

    aggregated_df_by_parent_company = df.groupby('parent_company').agg({
        'compset': lambda x: set(x),
        'compset_group': lambda x: set(x),
        'brand': lambda x: set(x),
        'company': lambda x: set(x)
    }).reset_index()

    return aggregated_df_by_brand, aggregated_df_by_company, aggregated_df_by_parent_company        



def check_likes_same(data, brand, date, compset_group):
    subset = data[(data['business_entity_doing_business_as_name'] == brand) & (data['compset_group'] == compset_group) & (data['period_end_date'] == date)]
    #Check if the value of 'likes' is the same for all rows
    if subset['likes'].nunique() == 1:
        return False
    else:
        return True

def plot_brands_compset(df, parent, list_of_parent, color="compset"):
    """
    Generates a parallel categories diagram for the specified brands.

    Args:
    df (DataFrame): A DataFrame containing the 'brand' and 'compset' columns.
    parent_list (list): A list of brands to visualize.
    color (str): name of relevant column

    Returns:
    None; displays a parallel categories plot.
    """
    # Filter the DataFrame for the selected brands
    df_long = df.explode('compset')
    df_long = df_long.explode('compset_group')
    dimensions = ['compset', 'compset_group', 'brand']

    if parent == 'company':
        df_long = df_long.explode('brand')
        dimensions.extend(['company'])
        
    elif parent == 'parent_company':
        df_long = df_long.explode('brand')
        df_long = df_long.explode("company")
        dimensions.extend(['company', 'parent_company'])
        
    compset_mapping = {v: i for i, v in enumerate(df_long[color].unique())}
    df_long['color'] = df_long[color].map(compset_mapping)  
    
    filtered_df = df_long[df_long[parent].isin(list_of_parent)]
    
    # Create the parallel categories diagram
    fig = px.parallel_categories(
        filtered_df, 
        dimensions=dimensions,
        labels={i: i for i in dimensions},
        color='color',
        color_continuous_scale=px.colors.sequential.Inferno
    )

    fig.update_layout(
        title='Parallel Categories Diagram for Selected Brands',
        width=800,
        height=500
    )

    # Display the plot
    fig.show()