import streamlit as st
import pandas as pd
import plotly.express as px
import processor,helper
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = processor.process()

st.sidebar.title('Olympic Analysis')
st.sidebar.image('download.png')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    
    years,country = helper.country_years_list(df)
    
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_Country = st.sidebar.selectbox('Select Country', country)
    
    medal = helper.fetch__medal_tally(df,selected_year,selected_Country)
    
    if selected_year == 'Overall' and selected_Country == 'Overall':
        st.header('Medal tally')
    if selected_year != 'Overall' and selected_Country == 'Overall':
        st.header('Medal tally in '+str(selected_year))
    if selected_year == 'Overall' and selected_Country != 'Overall':
        st.header('Medal tally of '+str(selected_Country))
    if selected_year != 'Overall' and selected_Country != 'Overall':
        st.header(str(selected_Country) + ' Performance in '+str(selected_year))
    
    st.table(medal)
    
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    Names = df['Name'].unique().shape[0]
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
        
    col4,col5,col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.title(events)
    with col5:
        st.header('Regions')
        st.title(nations)
    with col6:
        st.header('Atheletes')
        st.title(Names)
    
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating nations over the years")
    st.plotly_chart(fig)
    
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)
    
    athelete_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athelete_over_time, x="Edition", y="Name")
    st.title("Atheletes over the years")
    st.plotly_chart(fig)
    
    st.title('No. of Events over time for every Sports')
    plt,ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year','Event','Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(plt)
    
    st.title('Most succsessful atheletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sports_list)
    succsessful_ath = helper.most_succsessful(df, selected_sport)
    st.table(succsessful_ath)
    
if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Ananlysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    country_df = helper.yearswise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country+' Medal tally over the years')
    st.plotly_chart(fig)
    
    pt = helper.country_event_heatmap(df, selected_country)
    st.title(selected_country+" performance in the following sports")
    fig,ax = plt.subplots(figsize=(25,25))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)
    
    st.title('Top 10 Atheletes of '+selected_country)
    top10_df = helper.most_succsessful_countrywise(df,selected_country)
    st.table(top10_df)
    
if user_menu == 'Athlete wise Analysis':
    st.title('Distribution of Age')
    athelete_df = df.drop_duplicates(subset=['Name','region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()
    
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age', 'Gold Medalinst', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=550)
    st.plotly_chart(fig)
    
    st.title('Height vs Weight')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sports_list)
    
    temp_df = helper.weight_vs_height(df, selected_sport)
    fig,ax = plt.subplots(figsize=(25,25))
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'],style=temp_df['Sex'], s=60)
    st.pyplot(fig)
    
    st.title('Men vs Women participation over the Years')
    final = helper.men_vs_women(df)
    fig = fig = px.line(final, x='Year', y=['Male','Female'])
    st.plotly_chart(fig)