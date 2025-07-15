import pandas as pd
import numpy as np

def preprocess_data(athlete_df, noc_df):
    # Merge datasets
    df = athlete_df.merge(noc_df, on='NOC', how='left')
    
    # Clean medal data
    df['Medal'].fillna('No Medal', inplace=True)
    
    # Convert types
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Height'] = pd.to_numeric(df['Height'], errors='coerce')
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')
    
    return df

def medal_tally(df):
    # Create a copy of the dataframe
    medal_df = df.copy()
    
    # Initialize medal columns if they don't exist
    medal_df['Gold'] = 0
    medal_df['Silver'] = 0
    medal_df['Bronze'] = 0
    
    # Update medal counts
    medal_df.loc[medal_df['Medal'] == 'Gold', 'Gold'] = 1
    medal_df.loc[medal_df['Medal'] == 'Silver', 'Silver'] = 1
    medal_df.loc[medal_df['Medal'] == 'Bronze', 'Bronze'] = 1
    
    # Drop duplicates (keeping only unique medal entries per event)
    medal_df = medal_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    
    # Group by region and sum medals
    medal_tally = medal_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    
    # Calculate total medals
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    # Ensure all medal columns are integers
    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Total'] = medal_tally['Total'].astype(int)
    
    # Add additional statistics
    medal_tally['Gold_Ratio'] = (medal_tally['Gold'] / medal_tally['Total']).round(2)
    medal_tally['Silver_Ratio'] = (medal_tally['Silver'] / medal_tally['Total']).round(2)
    medal_tally['Bronze_Ratio'] = (medal_tally['Bronze'] / medal_tally['Total']).round(2)
    
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    
    return years, country

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    
    return x

def data_over_time(df, col):
    # Count unique events per year
    if col == 'Event':
        # Count unique events per year
        events_over_time = df.drop_duplicates(['Year', 'Event']).groupby('Year').count()['Event'].reset_index()
        events_over_time.rename(columns={'Year': 'Edition', 'Event': 'Count'}, inplace=True)
    else:
        # For other columns, count unique entries
        nations_over_time = df.drop_duplicates(['Year', col]).groupby('Year')[col].count().reset_index()
        nations_over_time.rename(columns={'Year': 'Edition', col: 'Count'}, inplace=True)
    
    # Sort by Edition
    result_df = nations_over_time.sort_values('Edition') if col != 'Event' else events_over_time
    return result_df


def most_successful(df, sport):
    # Filter for athletes with medals
    temp_df = df.dropna(subset=['Medal'])
    
    # Filter by sport if selected
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    # Count medals per athlete
    medal_counts = temp_df.groupby('Name')['Medal'].count().reset_index()
    medal_counts.rename(columns={'Medal': 'Medals'}, inplace=True)
    
    # Get athlete information
    athlete_info = temp_df[['Name', 'Sport', 'region']].drop_duplicates()
    
    # Merge medal counts with athlete information
    result = medal_counts.merge(athlete_info, on='Name', how='left')
    
    # Sort by medal count and take top 15
    result = result.sort_values('Medals', ascending=False).head(15)
    
    return result

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    
    pt = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    # Get successful athletes from the country
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    
    # Count medals per athlete
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Total_Medals']
    
    # Get sport information for each athlete
    athlete_info = temp_df[['Name', 'Sport']].drop_duplicates()
    
    # Merge medal counts with athlete information
    result = medal_counts.merge(athlete_info, on='Name', how='left')
    result = result.head(10)
    
    # Rename columns for clarity
    result = result[['Name', 'Sport', 'Total_Medals']]
    
    return result