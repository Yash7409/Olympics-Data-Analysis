import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from helper import preprocess_data, medal_tally, country_year_list, fetch_medal_tally, data_over_time, most_successful, yearwise_medal_tally, country_event_heatmap, most_successful_countrywise

# Define medal colors
MEDAL_COLORS = {
    '🥇': '#FFD700',  # Gold
    '🥈': '#C0C0C0',  # Silver
    '🥉': '#CD7F32',  # Bronze
    '🏅': '#FFD700'    # Total (using gold)
}

# Define medal emojis
MEDAL_EMOJIS = {
    'Gold': '🥇',
    'Silver': '🥈',
    'Bronze': '🥉',
    'Total': '🏅'
}

# Set page configuration
st.set_page_config(
    page_title="Olympic Games Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern and professional styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #000000;
        color: #ffffff;
    }
    
    .stDataFrame {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #424242;
    }
    
    .stMarkdown {
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    .stButton {
        background-color: #ffd700 !important;
        color: #000000 !important;
        border-radius: 8px;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton:hover {
        background-color: #ffcc00 !important;
        transform: translateY(-1px);
    }
    
    .medal-button {
        background-color: #ffd700 !important;
        color: #000000 !important;
        border-radius: 8px;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    
    .medal-button:hover {
        background-color: #ffcc00 !important;
        transform: translateY(-1px);
    }
    
    .stSelectbox, .stTextInput, .stNumberInput {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 0.75rem;
        border: 1px solid #424242;
        color: #ffffff;
        transition: all 0.2s ease-in-out;
    }
    
    .stSelectbox:hover, .stTextInput:hover, .stNumberInput:hover {
        border-color: #ffd700;
        box-shadow: 0 1px 3px rgba(255, 255, 255, 0.1);
    }
    
    .stPlotlyChart {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #424242;
    }
    
    .stTabs {
        margin-bottom: 1.5rem;
    }
    
    .stTab {
        padding: 1.5rem;
        background-color: #1a1a1a;
        border-radius: 12px;
        border: 1px solid #424242;
    }
    
    .medal-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .medal-icon {
        font-size: 2.5rem;
        color: #ffd700;
    }
    
    .medal-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .medal-stats {
        display: flex;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .medal-stat {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        background-color: #1a1a1a;
        border-radius: 8px;
        border: 1px solid #424242;
    }
    
    .medal-emoji {
        font-size: 1.25rem;
        color: #ffd700;
    }
    
    .medal-number {
        font-weight: 600;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Load and preprocess data
def load_data():
    athlete_df = pd.read_csv('athlete_events.csv')
    noc_df = pd.read_csv('noc_regions.csv')
    df = preprocess_data(athlete_df, noc_df)
    return df

df = load_data()

# Sidebar with improved styling
with st.sidebar:
    st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
        }
        .sidebar .sidebar-title {
            color: #008CBA;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .sidebar .radio-group {
            margin-bottom: 1rem;
        }
        .sidebar .selectbox {
            margin-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-title'>Olympics Analysis</div>", unsafe_allow_html=True)
    
    user_menu = st.radio(
        'Select an Option',
        ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'),
        key='menu_selection'
    )

# Main content with improved layout
if user_menu == 'Medal Tally':
    # Custom header with medal icon
    st.markdown("""
    <div class="medal-header">
        <div class="medal-icon">🏆</div>
        <h1 class="medal-title">Medal Tally Analysis</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with medal-themed filters
    with st.sidebar:
        st.markdown("""
        <div class="medal-header">
            <div class="medal-icon">🔍</div>
            <h3 class="medal-title">Filter Options</h3>
        </div>
        """, unsafe_allow_html=True)
        
        years, countries = country_year_list(df)
        selected_year = st.selectbox("Select Year", years)
        selected_country = st.selectbox("Select Country", countries)
    
    # Fetch medal tally
    medal_tally_df = fetch_medal_tally(df, selected_year, selected_country)
    
    # Main content
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.subheader("Global Medal Distribution")
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["Medal Table", "Medal Distribution", "Medal Type Analysis", "Regional Analysis"])
        
        with tab1:
            # Medal statistics header
            st.markdown("""
            <div class="medal-stats">
                <div class="medal-stat">
                    <span class="medal-emoji">🥇</span>
                    <span class="medal-number">{total_gold}</span>
                </div>
                <div class="medal-stat">
                    <span class="medal-emoji">🥈</span>
                    <span class="medal-number">{total_silver}</span>
                </div>
                <div class="medal-stat">
                    <span class="medal-emoji">🥉</span>
                    <span class="medal-number">{total_bronze}</span>
                </div>
                <div class="medal-stat">
                    <span class="medal-emoji">🏅</span>
                    <span class="medal-number">{total_medals}</span>
                </div>
            </div>
            """.format(
                total_gold=medal_tally_df['Gold'].sum(),
                total_silver=medal_tally_df['Silver'].sum(),
                total_bronze=medal_tally_df['Bronze'].sum(),
                total_medals=medal_tally_df['Total'].sum()
            ), unsafe_allow_html=True)
            
            st.markdown("### Global Medal Table")
            
            # Simple filters
            col1, col2 = st.columns(2)
            
            with col1:
                min_medals = st.number_input("Minimum Total Medals", min_value=0, max_value=1000, value=0)
            with col2:
                max_medals = st.number_input("Maximum Total Medals", min_value=0, max_value=1000, value=1000)
            
            # Apply filters
            filtered_df = medal_tally_df[(medal_tally_df['Total'] >= min_medals) & 
                                       (medal_tally_df['Total'] <= max_medals)]
            
            # Display table with medal-themed styling
            st.dataframe(
                filtered_df,
                column_config={
                    "region": st.column_config.TextColumn(
                        "Country",
                        help="Country name"
                    ),
                    "Gold": st.column_config.NumberColumn(
                        "Gold 🥇",
                        help="Number of gold medals",
                        format="%d 🥇"
                    ),
                    "Silver": st.column_config.NumberColumn(
                        "Silver 🥈",
                        help="Number of silver medals",
                        format="%d 🥈"
                    ),
                    "Bronze": st.column_config.NumberColumn(
                        "Bronze 🥉",
                        help="Number of bronze medals",
                        format="%d 🥉"
                    ),
                    "Total": st.column_config.NumberColumn(
                        "Total 🏅",
                        help="Total medals",
                        format="%d 🏅"
                    ),
                    "Gold_Ratio": st.column_config.NumberColumn(
                        "Gold Ratio",
                        help="Ratio of gold medals to total medals",
                        format="%.2f"
                    ),
                    "Silver_Ratio": st.column_config.NumberColumn(
                        "Silver Ratio",
                        help="Ratio of silver medals to total medals",
                        format="%.2f"
                    ),
                    "Bronze_Ratio": st.column_config.NumberColumn(
                        "Bronze Ratio",
                        help="Ratio of bronze medals to total medals",
                        format="%.2f"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Add summary statistics
            st.markdown("### Summary Statistics")
            st.write(f"**Total Countries:** {len(filtered_df)}")
            st.write(f"**Total Medals:** {filtered_df['Total'].sum():,}")
            st.write(f"**Average Medals per Country:** {filtered_df['Total'].mean():.1f}")
            st.write(f"**Top Medal Country:** {filtered_df.loc[filtered_df['Total'].idxmax(), 'region']}")
            st.write(f"**Most Gold Medals:** {filtered_df['Gold'].max()} 🥇")
            st.write(f"**Most Silver Medals:** {filtered_df['Silver'].max()} 🥈")
            st.write(f"**Most Bronze Medals:** {filtered_df['Bronze'].max()} 🥉")
            
        with tab2:
            st.markdown("### Medal Distribution by Country")
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.pie(medal_tally_df['Total'], labels=medal_tally_df['region'], 
                  autopct='%1.1f%%', textprops={'fontsize': 8})
            ax.set_title('Medal Distribution by Country')
            st.pyplot(fig)
            
            # Create bar chart for top 10 countries
            top_10 = medal_tally_df.head(10)
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(top_10['region'], top_10['Total'])
            ax.bar_label(bars)
            ax.set_title('Top 10 Countries by Total Medals')
            ax.set_xlabel('Country')
            ax.set_ylabel('Total Medals')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
            
        with tab3:
            st.markdown("### Medal Type Analysis")
            
            # Create stacked bar chart for medal types
            fig, ax = plt.subplots(figsize=(12, 6))
            medal_types = medal_tally_df[['Gold', 'Silver', 'Bronze']].head(10)
            
            # Plot stacked bars
            ax.bar(medal_tally_df['region'].head(10), medal_types['Gold'], label='Gold', color='gold')
            ax.bar(medal_tally_df['region'].head(10), medal_types['Silver'], 
                  bottom=medal_types['Gold'], label='Silver', color='silver')
            ax.bar(medal_tally_df['region'].head(10), medal_types['Bronze'], 
                  bottom=medal_types['Gold'] + medal_types['Silver'], 
                  label='Bronze', color='peru')
            
            ax.set_title('Medal Type Distribution for Top 10 Countries')
            ax.set_xlabel('Country')
            ax.set_ylabel('Number of Medals')
            plt.xticks(rotation=45, ha='right')
            ax.legend(title='Medal Type')
            st.pyplot(fig)
            
            # Create medal type ratio analysis
            medal_tally_df['Gold_Ratio'] = medal_tally_df['Gold'] / medal_tally_df['Total']
            medal_tally_df['Silver_Ratio'] = medal_tally_df['Silver'] / medal_tally_df['Total']
            medal_tally_df['Bronze_Ratio'] = medal_tally_df['Bronze'] / medal_tally_df['Total']
            
            st.markdown("### Medal Type Ratios")
            st.dataframe(medal_tally_df[['region', 'Gold_Ratio', 'Silver_Ratio', 'Bronze_Ratio']].head(10))
            
        with tab4:
            st.markdown("### Regional Analysis")
            
            # Group by continent (assuming 'region' contains continent information)
            continent_tally = medal_tally_df.groupby('region').sum().reset_index()
            
            # Create continent-wise medal distribution
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(continent_tally['region'], continent_tally['Total'])
            ax.set_title('Medal Distribution by Continent')
            ax.set_xlabel('Continent')
            ax.set_ylabel('Total Medals')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
            
            # Create continent-wise medal type distribution
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(continent_tally['region'], continent_tally['Gold'], label='Gold', color='gold')
            ax.bar(continent_tally['region'], continent_tally['Silver'], 
                  bottom=continent_tally['Gold'], label='Silver', color='silver')
            ax.bar(continent_tally['region'], continent_tally['Bronze'], 
                  bottom=continent_tally['Gold'] + continent_tally['Silver'], 
                  label='Bronze', color='peru')
            
            ax.set_title('Medal Type Distribution by Continent')
            ax.set_xlabel('Continent')
            ax.set_ylabel('Number of Medals')
            plt.xticks(rotation=45, ha='right')
            ax.legend(title='Medal Type')
            st.pyplot(fig)
        
        with tab1:
            st.markdown("### Medal Distribution by Country")
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.pie(medal_tally_df['Total'], labels=medal_tally_df['region'], 
                  autopct='%1.1f%%', textprops={'fontsize': 8})
            ax.set_title('Medal Distribution by Country')
            st.pyplot(fig)
            
            # Create bar chart for top 10 countries
            top_10 = medal_tally_df.head(10)
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(top_10['region'], top_10['Total'])
            ax.bar_label(bars)
            ax.set_title('Top 10 Countries by Total Medals')
            ax.set_xlabel('Country')
            ax.set_ylabel('Total Medals')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
            
        with tab2:
            st.markdown("### Medal Type Analysis")
            
            # Create stacked bar chart for medal types
            fig, ax = plt.subplots(figsize=(12, 6))
            medal_types = medal_tally_df[['Gold', 'Silver', 'Bronze']].head(10)
            
            # Plot stacked bars
            ax.bar(medal_tally_df['region'].head(10), medal_types['Gold'], label='Gold', color='gold')
            ax.bar(medal_tally_df['region'].head(10), medal_types['Silver'], 
                  bottom=medal_types['Gold'], label='Silver', color='silver')
            ax.bar(medal_tally_df['region'].head(10), medal_types['Bronze'], 
                  bottom=medal_types['Gold'] + medal_types['Silver'], 
                  label='Bronze', color='peru')
            
            ax.set_title('Medal Type Distribution for Top 10 Countries')
            ax.set_xlabel('Country')
            ax.set_ylabel('Number of Medals')
            plt.xticks(rotation=45, ha='right')
            ax.legend(title='Medal Type')
            st.pyplot(fig)
            
            # Create medal type ratio analysis
            medal_tally_df['Gold_Ratio'] = medal_tally_df['Gold'] / medal_tally_df['Total']
            medal_tally_df['Silver_Ratio'] = medal_tally_df['Silver'] / medal_tally_df['Total']
            medal_tally_df['Bronze_Ratio'] = medal_tally_df['Bronze'] / medal_tally_df['Total']
            
            st.markdown("### Medal Type Ratios")
            st.dataframe(medal_tally_df[['region', 'Gold_Ratio', 'Silver_Ratio', 'Bronze_Ratio']].head(10))
            
        with tab3:
            st.markdown("### Regional Analysis")
            
            # Group by continent (assuming 'region' contains continent information)
            continent_tally = medal_tally_df.groupby('region').sum().reset_index()
            
            # Create continent-wise medal distribution
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(continent_tally['region'], continent_tally['Total'])
            ax.set_title('Medal Distribution by Continent')
            ax.set_xlabel('Continent')
            ax.set_ylabel('Total Medals')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
            
            # Create continent-wise medal type distribution
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(continent_tally['region'], continent_tally['Gold'], label='Gold', color='gold')
            ax.bar(continent_tally['region'], continent_tally['Silver'], 
                  bottom=continent_tally['Gold'], label='Silver', color='silver')
            ax.bar(continent_tally['region'], continent_tally['Bronze'], 
                  bottom=continent_tally['Gold'] + continent_tally['Silver'], 
                  label='Bronze', color='peru')
            
            ax.set_title('Medal Type Distribution by Continent')
            ax.set_xlabel('Continent')
            ax.set_ylabel('Number of Medals')
            plt.xticks(rotation=45, ha='right')
            ax.legend(title='Medal Type')
            st.pyplot(fig)
            
    else:
        st.subheader("Selected Country/Year Analysis")
        
        # Display medal tally table
        st.dataframe(medal_tally_df)
        
        # Create medal type distribution chart
        fig, ax = plt.subplots(figsize=(8, 6))
        medals = medal_tally_df[['Gold', 'Silver', 'Bronze']].sum()
        ax.pie(medals, labels=['Gold', 'Silver', 'Bronze'], 
              colors=['gold', 'silver', 'peru'], autopct='%1.1f%%')
        ax.set_title('Medal Type Distribution')
        st.pyplot(fig)
        
        # Show medal trend over time if year is not 'Overall'
        if selected_year != 'Overall':
            country_df = yearwise_medal_tally(df, selected_country)
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(country_df['Year'], country_df['Medal'])
            ax.set_title(f'{selected_country} Medal Trend Over Time')
            ax.set_xlabel('Year')
            ax.set_ylabel('Number of Medals')
            st.pyplot(fig)

elif user_menu == 'Overall Analysis':
    st.header("Overall Analysis")
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Host Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    
    # Number of Events Over Time
    st.subheader("Number of Events Over Time")
    
    # Get events over time data
    events_over_time = data_over_time(df, 'Event')
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot with markers and line
    sns.lineplot(data=events_over_time, x='Edition', y='Count', marker='o', color='blue')
    
    # Add grid for better readability
    ax.grid(True, alpha=0.3)
    
    # Add title and labels with larger font
    ax.set_title('Number of Events Over Time', pad=20, fontsize=16)
    ax.set_xlabel('Olympic Edition', fontsize=14)
    ax.set_ylabel('Number of Events', fontsize=14)
    
    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45, ha='right')
    
    # Add data labels
    for x, y in zip(events_over_time['Edition'], events_over_time['Count']):
        ax.text(x, y, str(y), ha='center', va='bottom', fontsize=10)
    
    # Add trend line
    z = np.polyfit(events_over_time['Edition'], events_over_time['Count'], 1)
    p = np.poly1d(z)
    ax.plot(events_over_time['Edition'], p(events_over_time['Edition']), "r--", label='Trend Line')
    
    # Add legend
    ax.legend(title='Trend')
    
    # Add summary statistics
    st.markdown("### Summary Statistics")
    st.write(f"**Total Number of Events:** {events_over_time['Count'].sum()}")
    st.write(f"**Average Events per Edition:** {events_over_time['Count'].mean():.0f}")
    st.write(f"**Maximum Events:** {events_over_time['Count'].max()} (in {events_over_time.loc[events_over_time['Count'].idxmax(), 'Edition']})")
    
    st.pyplot(fig)
    
    # Most Successful Athletes
    st.subheader("Most Successful Athletes")
    
    # Create sport selection filter
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    
    # Get most successful athletes
    temp_df = most_successful(df, selected_sport)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Table View", "Visual Analysis"])
    
    with tab1:
        st.markdown("### Top Athletes Table")
        
        # Add medal emojis to the table
        temp_df['Medals'] = temp_df['Medals'].astype(str) + ' 🏅'
        
        # Display interactive table
        st.dataframe(
            temp_df,
            column_config={
                "Name": "Athlete Name",
                "Medals": "Total Medals 🏅",
                "Sport": "Sport",
                "region": "Country"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Add summary statistics
        st.markdown("### Summary Statistics")
        st.write(f"**Total Athletes:** {len(temp_df)}")
        st.write(f"**Total Medals:** {temp_df['Medals'].str.extract(r'(\d+)')[0].astype(int).sum()}")
        st.write(f"**Average Medals per Athlete:** {temp_df['Medals'].str.extract(r'(\d+)')[0].astype(int).mean():.1f}")
        
        # Add additional statistics
        st.markdown("### Additional Insights")
        st.write(f"**Most Medals by a Single Athlete:** {temp_df['Medals'].str.extract(r'(\d+)')[0].astype(int).max()} 🏅")
        st.write(f"**Most Successful Athlete:** {temp_df.loc[temp_df['Medals'].str.extract(r'(\d+)')[0].astype(int).idxmax(), 'Name']}")
        st.write(f"**Most Successful Country:** {temp_df['region'].value_counts().idxmax()}")
    
    with tab2:
        st.markdown("### Athlete Success Analysis")
        
        # Create bar chart for medals
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(temp_df['Name'], temp_df['Medals'].str.extract(r'(\d+)')[0].astype(int))
        
        # Add labels to bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height} 🏅',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Add country flags as markers
        for i, country in enumerate(temp_df['region']):
            ax.text(i, -1, f'({country})', ha='center', fontsize=10)
        
        ax.set_title(f'Top Athletes in {selected_sport if selected_sport != "Overall" else "All Sports"}')
        ax.set_xlabel('Athlete Name')
        ax.set_ylabel('Number of Medals')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        
        # Create pie chart for sport distribution
        if selected_sport == 'Overall':
            sport_dist = temp_df['Sport'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(sport_dist, labels=sport_dist.index, autopct='%1.1f%%')
            ax.set_title('Sport Distribution of Top Athletes')
            st.pyplot(fig)
        
        # Create medal type distribution
        if selected_sport == 'Overall':
            medal_types = df[df['Name'].isin(temp_df['Name'])]['Medal'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(medal_types, labels=medal_types.index, 
                  autopct='%1.1f%%', colors=['gold', 'silver', 'peru'])
            ax.set_title('Medal Type Distribution')
            st.pyplot(fig)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    
    nations_over_time = data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)
    
    events_over_time = data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)
    
    athlete_over_time = data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)
    
    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    temp_df = most_successful(df, selected_sport)
    st.table(temp_df)

elif user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    
    # Medal tally over years
    st.header(f"{selected_country} Medal Tally Over the Years")
    country_df = yearwise_medal_tally(df, selected_country)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(country_df['Year'], country_df['Medal'])
    ax.set_title(f'{selected_country} Medal Tally Over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Medals')
    st.pyplot(fig)
    
    # Sports performance heatmap
    st.header(f"{selected_country}'s Performance in Sports")
    pt = country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(pt, annot=True, cmap='viridis', ax=ax)
    ax.set_title(f'{selected_country} Sports Performance')
    st.pyplot(fig)
    
    # Top athletes
    st.header(f"Top 10 Athletes from {selected_country}")
    top10_df = most_successful_countrywise(df, selected_country)
    st.dataframe(top10_df)
    
    # Age distribution analysis
    athlete_df = df[df['region'] == selected_country]
    athlete_age = athlete_df['Age'].dropna()
    
    # Create histogram with more details
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot histogram with density curve
    sns.histplot(athlete_age, kde=True, ax=ax, bins=20)
    
    # Add mean and median lines
    mean_age = athlete_age.mean()
    median_age = athlete_age.median()
    ax.axvline(mean_age, color='red', linestyle='--', label=f'Mean: {mean_age:.1f}')
    ax.axvline(median_age, color='blue', linestyle='--', label=f'Median: {median_age:.1f}')
    
    # Add labels and title
    ax.set_title(f'Athlete Age Distribution for {selected_country}', pad=20)
    ax.set_xlabel('Age')
    ax.set_ylabel('Number of Athletes')
    
    # Add legend
    ax.legend()
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Show plot
    st.pyplot(fig)
    
    # Display summary statistics
    st.write('**Age Statistics:**')
    st.write(f'Mean Age: {mean_age:.1f} years')
    st.write(f'Median Age: {median_age:.1f} years')
    st.write(f'Standard Deviation: {athlete_age.std():.1f} years')

elif user_menu == 'Athlete-wise Analysis':
    st.header("Athlete-wise Analysis")
    
    # Age Analysis
    st.subheader("Age Analysis")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    
    # Age distribution by medal type
    st.markdown("### Age Distribution by Medal Type")
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.kdeplot(x1, label='Overall', ax=ax)
    sns.kdeplot(x2, label='Gold Medalists', ax=ax, color='gold')
    sns.kdeplot(x3, label='Silver Medalists', ax=ax, color='silver')
    sns.kdeplot(x4, label='Bronze Medalists', ax=ax, color='peru')
    
    ax.set_title('Age Distribution by Medal Type', pad=20)
    ax.set_xlabel('Age')
    ax.set_ylabel('Density')
    ax.legend()
    st.pyplot(fig)
    
    # Age distribution statistics
    st.markdown("### Age Statistics by Medal Type")
    age_stats = pd.DataFrame({
        'Overall': x1.describe(),
        'Gold Medalists': x2.describe(),
        'Silver Medalists': x3.describe(),
        'Bronze Medalists': x4.describe()
    }).T
    st.dataframe(age_stats)
    
    # Height vs Weight Analysis
    st.subheader("Height vs Weight Analysis")
    
    # Create sport selection filter
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    
    # Create athlete dataframe with necessary columns
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df = athlete_df[['Name', 'Sport', 'Sex', 'Height', 'Weight', 'Medal', 'region']]
    
    if selected_sport != 'Overall':
        # Filter by sport
        temp_df = athlete_df[athlete_df['Sport'] == selected_sport]
        
        # Create scatter plot with color-coded medals and gender
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot male athletes
        male_df = temp_df[temp_df['Sex'] == 'M']
        sns.scatterplot(data=male_df, x='Weight', y='Height', 
                       hue='Medal', style='Medal', 
                       palette={'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'peru'},
                       ax=ax, label='Male', s=100)
        
        # Plot female athletes
        female_df = temp_df[temp_df['Sex'] == 'F']
        sns.scatterplot(data=female_df, x='Weight', y='Height', 
                       hue='Medal', style='Medal', 
                       palette={'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'peru'},
                       ax=ax, label='Female', marker='x', s=100)
        
        # Add grid for better readability
        ax.grid(True, alpha=0.3)
        
        # Add annotations for notable athletes (top medal winners)
        notable_athletes = temp_df[temp_df['Medal'] != 'No Medal'].head(5)
        for _, athlete in notable_athletes.iterrows():
            ax.text(athlete['Weight'], athlete['Height'], 
                   athlete['Name'], fontsize=8, color='black', 
                   bbox=dict(facecolor='white', alpha=0.7, edgecolor='black'))
        
        # Add title and labels
        ax.set_title(f'Height vs Weight for {selected_sport}', pad=20, fontsize=16)
        ax.set_xlabel('Weight (kg)', fontsize=14)
        ax.set_ylabel('Height (cm)', fontsize=14)
        
        # Improve legend
        handles, labels = ax.get_legend_handles_labels()
        new_labels = ['Male', 'Female'] + labels[2:]
        ax.legend(handles[1:], new_labels, title='Category', fontsize=12)
        
        # Add correlation analysis
        corr = temp_df[['Height', 'Weight']].corr().iloc[0,1]
        st.write(f'**Correlation between Height and Weight:** {corr:.2f}')
        
        # Add statistical summary
        st.markdown("### Statistical Summary")
        stats = temp_df[['Height', 'Weight']].describe()
        st.dataframe(stats)
        
        # Add box plots for height and weight distribution
        st.markdown("### Distribution Analysis")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Height distribution
        sns.boxplot(data=temp_df, x='Sex', y='Height', ax=ax1)
        ax1.set_title('Height Distribution by Gender', pad=15)
        ax1.set_xlabel('Gender')
        ax1.set_ylabel('Height (cm)')
        
        # Weight distribution
        sns.boxplot(data=temp_df, x='Sex', y='Weight', ax=ax2)
        ax2.set_title('Weight Distribution by Gender', pad=15)
        ax2.set_xlabel('Gender')
        ax2.set_ylabel('Weight (kg)')
        
        st.pyplot(fig)
        
        st.pyplot(fig)
    else:
        st.write('Select a specific sport to view the analysis')
    
    # Gender Analysis
    st.subheader("Gender Analysis")
    final = athlete_df.drop_duplicates(subset=['Name', 'region', 'Year'])
    
    # Gender participation over years
    st.markdown("### Gender Participation Over the Years")
    final_men = final[final['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    final_women = final[final['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = final_men.merge(final_women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(final['Year'], final['Male'], label='Male', alpha=0.7)
    ax.bar(final['Year'], final['Female'], bottom=final['Male'], label='Female', alpha=0.7)
    
    ax.set_title('Gender Participation Over the Years', pad=20)
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Athletes')
    ax.legend()
    st.pyplot(fig)
    
    # Gender ratio analysis
    st.markdown("### Gender Ratio Analysis")
    final['Total'] = final['Male'] + final['Female']
    final['Female_Ratio'] = final['Female'] / final['Total'] * 100
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(final['Year'], final['Female_Ratio'], marker='o', color='purple')
    ax.set_title('Female Participation Ratio Over the Years', pad=20)
    ax.set_xlabel('Year')
    ax.set_ylabel('Female Ratio (%)')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    # Top Athletes Analysis
    st.subheader("Top Athletes Analysis")
    top_athletes = most_successful(df, 'Overall')
    
    # Create a detailed view of top athletes
    st.markdown("### Top Athletes by Medal Type")
    
    # Split by medal type
    gold_athletes = top_athletes[top_athletes['Medal'] == 'Gold']
    silver_athletes = top_athletes[top_athletes['Medal'] == 'Silver']
    bronze_athletes = top_athletes[top_athletes['Medal'] == 'Bronze']
    
    # Create tabs for different medal types
    tab1, tab2, tab3 = st.tabs(["Gold Medalists", "Silver Medalists", "Bronze Medalists"])
    
    with tab1:
        st.dataframe(gold_athletes)
        
    with tab2:
        st.dataframe(silver_athletes)
        
    with tab3:
        st.dataframe(bronze_athletes)
    
    # Sport distribution of top athletes
    st.markdown("### Sport Distribution of Top Athletes")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(data=top_athletes, x='Sport', hue='Medal', 
                 order=top_athletes['Sport'].value_counts().index,
                 palette={'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'peru'})
    ax.set_title('Sport Distribution of Top Athletes', pad=20)
    ax.set_xlabel('Sport')
    ax.set_ylabel('Number of Athletes')
    ax.legend(title='Medal Type')
    st.pyplot(fig)
    
    # Age distribution of top athletes
    st.markdown("### Age Distribution of Top Athletes")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.kdeplot(top_athletes['Age'].dropna(), ax=ax)
    ax.set_title('Age Distribution of Top Athletes', pad=20)
    ax.set_xlabel('Age')
    ax.set_ylabel('Density')
    st.pyplot(fig)
    
    # Create a bar chart for top athletes
    fig, ax = plt.subplots(figsize=(12, 8))
    # Sort athletes by total medals
    top_athletes = top_athletes.sort_values('Total', ascending=False)
    
    # Create stacked bars for each medal type
    ax.bar(top_athletes['Name'], top_athletes['Gold'], label='Gold', color='gold')
    ax.bar(top_athletes['Name'], top_athletes['Silver'], bottom=top_athletes['Gold'], label='Silver', color='silver')
    ax.bar(top_athletes['Name'], top_athletes['Bronze'], 
          bottom=top_athletes['Gold'] + top_athletes['Silver'], 
          label='Bronze', color='peru')
    
    # Add labels and title
    ax.set_title('Top 10 Most Successful Athletes', pad=20)
    ax.set_xlabel('Athlete Name')
    ax.set_ylabel('Number of Medals')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add legend
    ax.legend(title='Medal Type')
    
    # Add total medal count above each bar
    for i, row in top_athletes.iterrows():
        total = row['Total']
        ax.text(i, total + 0.5, str(total), ha='center', va='bottom', fontweight='bold')
    
    # Add grid for better readability
    ax.grid(True, axis='y', alpha=0.3)
    
    # Show the plot
    st.pyplot(fig)
    
    # Also show the raw data
    st.dataframe(top_athletes)