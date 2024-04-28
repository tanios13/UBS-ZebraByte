import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def brand_level_trends(data, brand):

    compset_group = data[data['business_entity_doing_business_as_name'] == brand]['compset_group'].unique()
    compsets = data[data['business_entity_doing_business_as_name'] == brand]['compset'].unique()
    dates = data[(data['business_entity_doing_business_as_name'] == brand) & (data['compset'] == compsets[0])]['period_end_date'].unique()

    trends_all = np.empty((len(compsets), 5, len(dates)))
    trends_brand = np.empty((5, len(dates)))
    trends_cumulative = np.zeros((trends_all.shape[1], trends_all.shape[2]))

    for i in range(len(compsets)):
        
        subset_all = data[(data['business_entity_doing_business_as_name'] == 'All Brands') & (data['compset'] == compsets[i]) & (data['period_end_date'].isin(dates)) & (data['compset_group'] == compset_group[0])]  # Ajoutez cette condition
        subset_all = subset_all.sort_values('period_end_date')

        trends_all[i, 0] = (subset_all['likes'] - subset_all['likes'].min()) / ((subset_all['likes'].max() - subset_all['likes'].min()))
        trends_all[i, 1] = (subset_all['comments'] - subset_all['comments'].min()) / ((subset_all['comments'].max() - subset_all['comments'].min()))
        trends_all[i, 2] = (subset_all['videos'] - subset_all['videos'].min()) / ((subset_all['videos'].max() - subset_all['videos'].min()))
        trends_all[i, 3] = (subset_all['pictures'] - subset_all['pictures'].min()) / ((subset_all['pictures'].max() - subset_all['pictures'].min()))
        trends_all[i, 4] = (subset_all['followers'] - subset_all['followers'].min()) / ((subset_all['followers'].max() - subset_all['followers'].min()))
        trends_cumulative += trends_all[i]

        if i == 0:
            subset_brand = data[(data['business_entity_doing_business_as_name'] == brand) & (data['compset'] == compsets[i]) & (data['period_end_date'].isin(dates)) & (data['compset_group'] == compset_group[0])]  # Ajoutez cette condition
            subset_brand = subset_brand.sort_values('period_end_date')
            
            trends_brand[0] = (subset_brand['likes'] - subset_brand['likes'].min()) / ((subset_brand['likes'].max() - subset_brand['likes'].min()))
            trends_brand[1] = (subset_brand['comments'] - subset_brand['comments'].min()) / ((subset_brand['comments'].max() - subset_brand['comments'].min()))
            trends_brand[2] = (subset_brand['videos'] - subset_brand['videos'].min()) / ((subset_brand['videos'].max() - subset_brand['videos'].min()))
            trends_brand[3] = (subset_brand['pictures'] - subset_brand['pictures'].min()) / ((subset_brand['pictures'].max() - subset_brand['pictures'].min()))
            trends_brand[4] = (subset_brand['followers'] - subset_brand['followers'].min()) / ((subset_brand['followers'].max() - subset_brand['followers'].min()))
            
    return trends_brand, trends_all, trends_cumulative/trends_all.shape[0], dates

def plot_metrics_individual(trends_brand, trends_all, dates):
    metrics = ['likes', 'comments', 'videos', 'pictures', 'followers']
    fig, axs = plt.subplots(5, 1, figsize=(10, 10))
    
    for i in range(5):
        axs[i].plot(dates, trends_brand[i], label=f'{metrics[i]} (brand)')
        axs[i].plot(dates, trends_all[0, i], label=f'{metrics[i]} (all brands)')
        axs[i].set_title(f'Trends for {metrics[i]}')
        axs[i].set_xlabel('Date')
        axs[i].set_ylabel('Value')
        axs[i].legend()
        axs[i].xaxis.set_major_locator(mdates.MonthLocator(interval=12))
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    plt.tight_layout()
    plt.show()

def plot_metrics_total(trends_brand, trends_cumulative, dates):
    metrics = ['likes', 'comments', 'videos', 'pictures', 'followers']
    fig, axs = plt.subplots(5, 1, figsize=(10, 10))  # Change figsize here

    for i in range(5):
        axs[i].plot(dates, trends_brand[i], label=f'{metrics[i]} (brand)')
        axs[i].plot(dates, trends_cumulative[i], label=f'{metrics[i]} (all brands)')

        axs[i].set_title(f'Trends for {metrics[i]} cumulated over all compsets')
        axs[i].set_xlabel('Date')
        axs[i].set_ylabel('Value')
        axs[i].legend()

        axs[i].xaxis.set_major_locator(mdates.MonthLocator(interval=12))
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.tight_layout()
    plt.show()

    