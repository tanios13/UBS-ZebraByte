import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_brand(data, brand='Versace', compset='Soft Luxury', metric='likes'):
    # Extraire les lignes pour la marque et le compset spécifiés et les trier par 'period_end_date', puis tracer la métrique au fil du temps
    subset = data[(data['business_entity_doing_business_as_name'] == brand) & (data['compset'] == compset)]
    
    # Convertir 'period_end_date' en datetime
    subset.loc[:, 'period_end_date'] = pd.to_datetime(subset['period_end_date'])
    
    subset = subset.sort_values('period_end_date')
    
    fig, ax = plt.subplots()
    ax.plot(subset['period_end_date'], subset[metric])
    
    # Définir le format de l'axe des x pour afficher une marque tous les 3 mois
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    # Rendre les labels de l'axe des x verticaux
    plt.xticks(rotation='vertical')
    plt.xlabel('Date')
    plt.ylabel(metric)
    plt.title(f'{metric} for {brand} in the {compset} compset group')
    plt.show()


def plot_brand_per_pictures(data, brand='Versace', compset='Soft Luxury', metric='likes', num_pictures='num_pictures'):
    # Extraire les lignes pour la marque et le compset spécifiés et les trier par 'period_end_date', puis tracer la métrique au fil du temps
    subset = data[(data['business_entity_doing_business_as_name'] == brand) & (data['compset'] == compset)]
    
    # Convertir 'period_end_date' en datetime
    subset.loc[:, 'period_end_date'] = pd.to_datetime(subset['period_end_date'])
    
    # Calculer les likes par image
    subset['likes_per_picture'] = subset[metric] / subset[num_pictures]
    
    subset = subset.sort_values('period_end_date')
    
    fig, ax = plt.subplots()
    ax.plot(subset['period_end_date'], subset['likes_per_picture'])
    
    # Définir le format de l'axe des x pour afficher une marque tous les 3 mois
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    
    # Rendre les labels de l'axe des x verticaux
    plt.xticks(rotation='vertical')
    plt.xlabel('Date')
    plt.ylabel('Likes per picture')
    plt.title(f'Likes per picture for {brand} in the {compset} compset group')
    plt.show()


def plot_brands(data, brands=['All Brands', 'Gucci'], compset='Soft Luxury', metric='likes', num_pictures='pictures', plot_difference=False):
    fig, axs = plt.subplots(2, 1, sharex=True) if plot_difference else plt.subplots(1, 1)
    axs = [axs] if not plot_difference else axs
    subsets = []
    
    for brand in brands:
        subset = data[(data['business_entity_doing_business_as_name'] == brand) & (data['compset'] == compset)].copy()  # Créer une copie explicite ici
        subset.loc[:, 'period_end_date'] = pd.to_datetime(subset['period_end_date'])
        subset['likes_per_picture'] = subset[metric] / subset[num_pictures]
        subset['likes_per_picture'] = (subset['likes_per_picture'] - subset['likes_per_picture'].min()) / (subset['likes_per_picture'].max() - subset['likes_per_picture'].min())
        subset = subset.sort_values('period_end_date')
        subsets.append(subset)
        axs[0].plot(subset['period_end_date'], subset['likes_per_picture'], label=brand)
    
    if plot_difference and len(subsets) == 2:
        difference = subsets[1]['likes_per_picture'].values - subsets[0]['likes_per_picture'].values
        axs[1].plot(subsets[0]['period_end_date'], difference, label='Difference')
        axs[1].set_ylabel('Difference')
        axs[1].legend()
    
    axs[0].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation='vertical')
    axs[0].set_ylabel('Normalized likes per picture')
    axs[0].set_title(f'Normalized likes per picture for different brands in the {compset} compset group')
    axs[0].legend()
    plt.show()


def legal_entity_summary(data, legal_entity='Capri Holdings'):
    # Take a legal_entity and display all business_entity_doing_business_as_name
    # Calculate total likes, comments, followers, pictures, and videos for the legal_entity for each timestamp
    subset = data[data['legal_entity_name'] == legal_entity]
    summary = subset.groupby('period_end_date').agg({
        'likes': 'sum',
        'comments': 'sum',
        'followers': 'sum',
        'pictures': 'sum',
        'videos': 'sum'
    }).reset_index()  # Ajoutez .reset_index() ici
    return summary


def plot_entity(data, summary, entity, brand='All brands', compset='Soft Luxury', metric='likes', num_pictures='pictures', plot_difference=False):
    fig, axs = plt.subplots(2, 1, sharex=True) if plot_difference else plt.subplots(1, 1)
    axs = [axs] if not plot_difference else axs

    subset = data[(data['business_entity_doing_business_as_name'] == brand) & (data['compset'] == compset)].copy()  # Créer une copie explicite ici
    subset.loc[:, 'period_end_date'] = pd.to_datetime(subset['period_end_date'])
    subset['likes_per_picture'] = subset[metric] / subset[num_pictures]
    subset['likes_per_picture'] = (subset['likes_per_picture'] - subset['likes_per_picture'].min()) / (subset['likes_per_picture'].max() - subset['likes_per_picture'].min())
    subset = subset.sort_values('period_end_date')
    axs[0].plot(subset['period_end_date'], subset['likes_per_picture'], label=brand)

    summary.loc[:, 'period_end_date'] = pd.to_datetime(summary['period_end_date'])
    summary = summary.sort_values('period_end_date')
    summary['likes_per_picture'] = summary['likes'] / summary['pictures']
    summary['likes_per_picture'] = (summary['likes_per_picture'] - summary['likes_per_picture'].min()) / (summary['likes_per_picture'].max() - summary['likes_per_picture'].min())
    axs[0].plot(summary['period_end_date'], summary['likes_per_picture'], label=entity)
    
    if plot_difference:
        difference = summary['likes_per_picture'].values - subset['likes_per_picture'].values
        axs[1].plot(summary['period_end_date'], difference, label='Difference')
        axs[1].set_ylabel('Difference')
        axs[1].legend()
    
    axs[0].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation='vertical')
    axs[0].set_ylabel('Normalized likes per picture')
    axs[0].set_title(f'Normalized likes per picture for different brands in the {compset} compset group')
    axs[0].legend()
    plt.show()