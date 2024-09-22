import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

zomato=pd.read_csv("https://raw.githubusercontent.com/nethajinirmal13/Training-datasets/main/zomato/zomato.csv")

url = "https://raw.githubusercontent.com/nethajinirmal13/Training-datasets/main/zomato/Country-Code.xlsx"
country = pd.read_excel(url, engine='openpyxl')

zomato['Cuisines'].fillna('Not Specified',inplace=True)

zomato_df=zomato.drop(columns=['Longitude','Latitude','Restaurant ID','Locality Verbose','Switch to order menu',"Address"])

zomato_df.rename({'Restaurant Name':'Restaurant_Name',
                  'Country Code':'Country_Code',
                  'Average Cost for two':'Average_Cost_for_two',
                  'Has Table booking':'Table_Booking',
                  'Has Online delivery':'Onlne_Delivery',
                  'Is delivering now':'Delivering_now',
                  'Price range':'Price_Range',
                  'Aggregate rating':'Aggregate_Rating',
                  'Rating color':'Rating_Color',
                  'Rating text':'Comments'})

df = zomato_df.merge(country, on='Country Code', how='right')

df.to_csv('zomato_df.csv',index=False)

st.set_page_config(page_title="ZOMATO DATA ANALYSIS AND VISUALIZATION",layout="wide")
st.header("ZOMATO DATA ANALYSIS AND VISUALIZATION")
tab1,tab2,tab3=st.tabs(["Introduction","Data Exploration","Insights"])
default_option="Introduction"

with tab1:
    col1,col2,col3 = st.columns([6,0.1,6])
    with col1:
        st.write("")
        st.image(Image.open("C:\\Users\\prave\\Downloads\\zomato.jpeg"), width=500)
        st.write("#### :red[**Technologies Used :**] Python, Pandas,plotly, Streamlit")
    
    with col3:
        st.write("#### :red[**Overview :**] The Zomato Data Analysis and Visualization project aims to explore and analyze Zomato's restaurant and customer data to derive insights into user behavior, preferences, and trends in the restaurant industry. By using Python scripting, Pandas, and Plotly, this project focuses on analyzing the available data to provide useful insights to stakeholders, such as restaurants and investors, through a visually interactive dashboard.")
        

with tab2:
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Country', data=df, palette='viridis') 
    plt.title('Distribution of Country')
    plt.xlabel('Country')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    st.pyplot(plt)

    st.write("### Key Insights")
    st.write("From the above chart, it is clear that **India** has the highest number of restaurants.")

    st.header("REVIEW ANALYSIS")
    col1,col2=st.columns(2)
    with col1:
        ratings=df.groupby(['Aggregate rating','Rating color', 'Rating text']).size().reset_index().rename(columns={0:'Rating Count'})
        st.dataframe(ratings)

    with col2:
        st.write("We can easily observe the table and find how the ratings are distributed:")
        st.write("Rating 0 - white - Not rated")
        st.write("Rating 1.8 to 2.4 - red - poor")
        st.write("Rating 2.5 to 3.4 - orange - Average")
        st.write("Rating 3.5 to 3.9 - Yellow - Good")
        st.write("Rating 4.0 to 4.4 - Green - Very Good")
        st.write("Rating 4.5 to 4.9 - Dark Green - Excellent")

    col1,col2=st.columns(2)
    with col1:    
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        plt.figure(figsize=(12,6))
        sns.barplot(x='Aggregate rating',y='Rating Count',data=ratings, hue= 'Rating color', palette=['lightpink','red','orange','yellow','green','darkgreen'])
        st.pyplot(plt)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("### Key Insights")
        st.write("The majority of restaurants have an **aggregate rating** in the range of **3.0 to 3.9**, indicating that most restaurants are rated as 'Good'. The number of restaurants with higher ratings is relatively low.")

    with col2:
        fig = px.bar(ratings, 
                        x='Rating color', 
                        color='Rating text',
                    y='Rating Count', 
                        color_discrete_sequence=['lightpink', 'Red','Orange','Yellow','Green',"Darkgreen"], 
                        title='Rating Distribution')
        st.plotly_chart(fig)
        st.write("### Key Insights")
        st.write("Among all the restaurants, those with an **orange rating (average)**, falling between **2.5 and 3.4**, are the most common. However, there is a high number of **unrated restaurants**, which requires further investigation to understand the cause.")

    col1,col2=st.columns(2)
    with col1:
        st.write("COUNTRY WHICH HAS NO RATINGS:")
        no_rated=df[df['Rating color']=="White"].groupby("Country").size().reset_index().rename(columns={0:'N0_Rating Count'})
        no_rated
        
    with col2:
        st.write("COUNTRY AND THEIR RESPECTIVE CURRENCY:")
        country_currency = df[['Country','Currency']].groupby(['Country','Currency']).size().reset_index(name='count').drop('count', axis=1, inplace=False)
        country_currency
    


    col1,col2=st.columns(2)
    with col1:
        online_delivery_count = df[df['Has Online delivery'] == 'Yes'].groupby('Country').size().reset_index().rename(columns={0:'Online_delivery_count'})
        fig = px.pie(online_delivery_count, 
                names='Country', 
                values='Online_delivery_count',  
                title='Country having Online Delivery')
        st.plotly_chart(fig)
        st.write("### Key Insights")
        st.write("**India** and **UAE** are the only countries offering online delivery, with **India** accounting for **98.9%** and **UAE** for **1.14%** of the total online delivery orders.")

    with col2:
        dine_in_count = df[df['Has Table booking'] == 'Yes'].groupby('Country').size().reset_index().rename(columns={0:'Dine-in-count'})
        fig = px.pie(dine_in_count, 
                names='Country', 
                values='Dine-in-count',  
                title='Country having Table booking')
        st.plotly_chart(fig)
        st.write("### Key Insights")
        st.write("**India**, **UAE**, **Philippines**, **United Kingdom**, **South Africa**, and **Qatar** are the countries where table booking is preferred. **India** ranks first with **95.9%** of table bookings, followed by **UAE** at **1.55%**, and **Philippines** at **1.21%**.")

    

    st.header("INDIA ANALYSIS")

    
    india_data = df[df['Country'] == 'India']

    
    restaurant_review = india_data[['Restaurant Name', 'Aggregate rating']].sort_values(by='Aggregate rating', ascending=False)
    restaurant_review = restaurant_review.head(20)

    fig = px.bar(restaurant_review, 
                x='Restaurant Name', 
                y='Aggregate rating',
                title='Top Rated Restaurants in India',
                color_discrete_sequence=px.colors.sequential.Redor_r)
    fig.update_layout(yaxis=dict(range=[0, 5]))
    st.plotly_chart(fig)
    st.write("### Key Insights")
    st.write("The highest-rated restaurants are **AN's-Absolute Barbecues**, **Naturals Ice Cream**, and **Zolocrust - Hotel Clarks Amer**, with aggregate ratings of 4.9.")
    
    costly_restaurant = india_data[['Restaurant Name','Average Cost for two','Cuisines','City','Aggregate rating']].sort_values(by='Average Cost for two',ascending=False)  
    costly_restaurant = costly_restaurant.head(20)
    fig = px.bar(costly_restaurant, 
            x='Restaurant Name', 
            y='Average Cost for two',
            title='Costly Restaurants in India',
            hover_data=['Cuisines','City','Aggregate rating'],
            color_discrete_sequence=px.colors.sequential.Redor_r)
    fig.update_layout(
        xaxis_tickangle=-45,  
        xaxis_title='Restaurant Name',
        yaxis_title='Average Cost for two',
        title_x=0.5 
    )
    st.plotly_chart(fig)
    st.write("### Key Insights")
    st.write("The most expensive restaurants based on the 'Average Cost for Two' are **Orient Express - Taj Palace Hotel**, **Tian - Asian Cuisine Studio - ITC Maurya**, and **Bukhara - ITC Maurya**, with average costs of Rs. 8000, Rs. 7000, and Rs. 6500 for two people, respectively.")
    

    col1,col2=st.columns(2)
    with col1:
        costly_cuisines = india_data[['Cuisines','Average Cost for two','Restaurant Name','City','Aggregate rating']].sort_values(by='Average Cost for two',ascending=False).head(5)
        fig_cuisines=px.scatter(costly_cuisines, 
                                x="Cuisines", 
                                y="Average Cost for two", 
                                title='Costly cuisines in India', 
                                hover_data=['Restaurant Name','City','Aggregate rating'],    
                                template='plotly_dark')
        st.plotly_chart(fig_cuisines)
        st.write("### Key Insights")
        st.write("The most expensive cuisines based on the 'Average Cost for Two' are **European**, **Asian (Japanese, Korean, Thai, Chinese)**, and **North Indian**, with average costs of Rs. 8000, Rs. 7000, and Rs. 6500 for two people, respectively.")
    
    with col2:
        costly_cuisines = india_data[['Cuisines','Average Cost for two','Restaurant Name','City','Aggregate rating']].sort_values(by='Average Cost for two',ascending=False).tail(5)
        fig_cuisines=px.scatter(costly_cuisines, 
                                x="Cuisines", 
                                y="Average Cost for two", 
                                title='Least Expensive cuisines in India', 
                                hover_data=['Restaurant Name','City','Aggregate rating'],    
                                template='plotly_dark')
        st.plotly_chart(fig_cuisines)
        st.write("### Key Insights")
        st.write("The least expensive cuisines based on the 'Average Cost for Two' are **Chinese, North Indian, Fast Food**, **Cafe, Italian, Mexican, North Indian, Continental**, **Street Food**, and **Cafe, North Indian, Chinese**, with average costs starting from Rs. 0 for two people.")


    online_delivery_count = india_data[india_data['Has Online delivery'] == 'Yes']['Restaurant Name'].count()
    dine_in_count = india_data[india_data['Has Table booking'] == 'Yes']['Restaurant Name'].count()
    delivery_vs_dinein = pd.DataFrame({
        'Service': ['Online Delivery', 'Dine-in'],
        'Count': [online_delivery_count, dine_in_count]
    })
    fig = px.pie(delivery_vs_dinein, 
                names='Service', 
                values='Count', 
                title='Online Delivery vs Dine-in in India',
                color_discrete_sequence=['lightblue', 'lightgreen'])
    st.plotly_chart(fig)
    st.write("### Key Insights")
    st.write("In India, **68.6%** of customers prefer **online delivery**, while **31.4%** prefer **table booking**.")
    
    
    col1,col2=st.columns(2)
    with col1:
        Indiavote=india_data[['Votes','Restaurant Name','City']].sort_values(by='Votes', ascending=False).reset_index(drop=True).head(5)
        st.write('Restaurant with High vote', Indiavote)

    with col2:
        Indiavote1=india_data[['Votes','Restaurant Name','City']].sort_values(by='Votes', ascending=False).reset_index(drop=True).tail(5)
        st.write('Restaurant which has less vote', Indiavote1)

    st.write("### Key Insights")
    st.write("The top 3 highest voted restaurants are **Toit**, **Truffles**, and **Hauz Khas Social**, while the least voted are **TAG**, **Urban Patty House**, and **Rasoi - The Indian Zaika**.")

    
    city = st.selectbox("Select City", india_data['City'].unique())
    city_data = india_data[india_data['City'] == city]

    famous_cuisines = city_data['Cuisines'].value_counts().head(20).reset_index()

    figure_cuisines=px.bar(famous_cuisines,x='Cuisines', y='count',title=f'Famous Cuisines in {city}')
    figure_cuisines.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(figure_cuisines)
    
    col1,col2=st.columns(2)
    with col1:
        costlier_cuisine = city_data[['Cuisines','Average Cost for two','Restaurant Name','Aggregate rating']].sort_values(by="Average Cost for two",ascending=False).head(5)
        fig_cuisines=px.scatter(costlier_cuisine, 
                                x="Cuisines", 
                                y="Average Cost for two", 
                                title=f'Costly cuisines in {city}', 
                                hover_data=['Restaurant Name','Aggregate rating'],    
                                template='plotly_dark')
        st.plotly_chart(fig_cuisines)
    
    with col2:
        costlier_cuisine = city_data[['Cuisines','Average Cost for two','Restaurant Name','Aggregate rating']].sort_values(by="Average Cost for two",ascending=False).tail(5)
        fig_cuisines=px.scatter(costlier_cuisine, 
                                x="Cuisines", 
                                y="Average Cost for two", 
                                title=f'Least Expensive cuisines in {city}', 
                                hover_data=['Restaurant Name','Aggregate rating'],    
                                template='plotly_dark')
        st.plotly_chart(fig_cuisines)

    col1,col2=st.columns(2)
    with col1:
        costly_restaurant = city_data[['Restaurant Name','Average Cost for two','Cuisines','Aggregate rating']].sort_values(by='Average Cost for two',ascending=False)
        costly_restaurant = costly_restaurant.head(5)
        fig = px.bar(costly_restaurant, 
                x='Restaurant Name', 
                y='Average Cost for two',
                title=f'Costly Restaurants in {city}',
                hover_data=['Cuisines','Aggregate rating'],
                color_discrete_sequence=px.colors.sequential.Redor_r)
        fig.update_layout(
            xaxis_tickangle=-45,  
            xaxis_title='Restaurant Name',
            yaxis_title='Average Cost for two',
            title_x=0.5 
        )
        st.plotly_chart(fig)
    with col2:
        costly_restaurant = city_data[['Restaurant Name','Average Cost for two','Cuisines','Aggregate rating']].sort_values(by='Average Cost for two',ascending=False)
        costly_restaurant = costly_restaurant.tail(5)
        fig = px.bar(costly_restaurant, 
                x='Restaurant Name', 
                y='Average Cost for two',
                title=f'Least Expensive Restaurants in {city}',
                hover_data=['Cuisines','Aggregate rating'],
                color_discrete_sequence=px.colors.sequential.Redor_r)
        fig.update_layout(
            xaxis_tickangle=-45,  
            xaxis_title='Restaurant Name',
            yaxis_title='Average Cost for two',
            title_x=0.5 
        )
        st.plotly_chart(fig)

    online_delivery_count = city_data[city_data['Has Online delivery'] == 'Yes']['Restaurant Name'].count()
    dine_in_count = city_data[city_data['Has Table booking'] == 'Yes']['Restaurant Name'].count()
    delivery_vs_dinein = pd.DataFrame({
        'Service': ['Online Delivery', 'Dine-in'],
        'Count': [online_delivery_count, dine_in_count]
    })
    fig = px.pie(delivery_vs_dinein, 
                names='Service', 
                values='Count', 
                title=f'Online Delivery vs Dine-in in {city}')
    st.plotly_chart(fig)

    col1,col2=st.columns(2)
    with col1:
        cityvote=city_data[['Votes','Restaurant Name','Cuisines']].sort_values(by='Votes', ascending=False).reset_index(drop=True).head(5)
        st.write('Restaurant with High vote', cityvote)

    with col2:
        cityvote1=city_data[['Votes','Restaurant Name','Cuisines']].sort_values(by='Votes', ascending=False).reset_index(drop=True).tail(5)
        st.write('Restaurant which has less vote', cityvote1)

    india_data = df[df['Country'] == 'India']
    city_comparison=india_data.groupby('City')['Average Cost for two'].mean().sort_values(ascending=False).reset_index()
    fig_city=px.line(city_comparison,x='City',y='Average Cost for two',
                        title='Price comparison on cities',template='plotly_dark')
    st.plotly_chart(fig_city)
    
    col1,col2=st.columns(2)
    with col1:
        high_living_cost = india_data.groupby('City')['Average Cost for two'].mean().sort_values(ascending=False).head()
        st.write('Cities with High Living Costs', high_living_cost)

    with col2:
        low_living_cost = india_data.groupby('City')['Average Cost for two'].mean().sort_values(ascending=True).head()
        st.write('Cities with Low Living Costs', low_living_cost)

    
    india_data = df[df['Country'] == 'India']
    online_deli=india_data[india_data['Has Online delivery']=='Yes'].groupby('City')['Average Cost for two'].mean().sort_values(ascending=False).reset_index()
    fig_online=px.scatter(online_deli,x='City',y='Average Cost for two',title='Which Part of India Spends More on Online Delivery',template='plotly_dark')
    st.plotly_chart(fig_online)
    st.write("### Key Insights")
    st.write("In **India**, cities like **Pune**, **Hyderabad**, and **Bangalore** spend the most on online delivery, based on the average cost for two.")

    india_data = df[df['Country'] == 'India']
    offline_deli=india_data[india_data['Has Table booking']=='Yes'].groupby('City')['Average Cost for two'].mean().sort_values(ascending=False).reset_index()
    fig_offline=px.scatter(offline_deli,x='City',y='Average Cost for two',title='Which Part of India Spends More on Dine_in',template='plotly_dark')
    st.plotly_chart(fig_offline)
    st.write("### Key Insights")
    st.write("In **India**, cities like **Ghaziabad**, **New Delhi**, and **Gurgaon** spend the most on table bookings (dine-in), based on the average cost for two.")
    
    country = st.selectbox("Select Country", df['Country'].unique())
    country_data = df[df['Country'] == country]

    cuisines_counts = country_data['Cuisines'].value_counts().reset_index().head(30)
    
    fig_cuisines_famous=px.scatter(cuisines_counts,x='Cuisines', y='count',
                                   title=f'Famous Cuisines in {country}',template='plotly_dark')
    fig_cuisines_famous.update_layout(
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_cuisines_famous)

    cost_cuisines=country_data[['Cuisines','Average Cost for two','City','Currency','Restaurant Name','Aggregate rating']].sort_values(by='Average Cost for two',ascending=False).head(20)
    fig_cuisines=px.scatter(cost_cuisines, 
                            x="Cuisines", 
                            y="Average Cost for two", 
                            title=f'Costly cuisines in {country}]',
                            hover_data=['Restaurant Name','Aggregate rating','City','Currency'],     
                            template='plotly_dark')
    st.plotly_chart(fig_cuisines)
    

    df_scatter = country_data[['Restaurant Name','Aggregate rating','Cuisines','Average Cost for two','City','Currency']].sort_values(by='Aggregate rating', ascending=False)
    df_scatter= df_scatter.head(10)
    fig_scatter = px.scatter(df_scatter, 
                            x="Restaurant Name", 
                            y="Aggregate rating", 
                            title='Restaurant with high review rating', 
                            hover_data=['Cuisines','Average Cost for two','City','Currency'], 
                            template='plotly_dark')
    st.plotly_chart(fig_scatter)

    df_scatter = country_data[['Restaurant Name', 'Average Cost for two','Aggregate rating','Cuisines','City']].sort_values(by='Average Cost for two', ascending=False).head(10)
    fig_costlier=px.line(df_scatter,x="Restaurant Name",y='Average Cost for two',title="costly Restaurants",template='plotly_dark',hover_data=['Aggregate rating','Cuisines','City'])
    st.plotly_chart(fig_costlier)

    online_delivery_count = country_data[country_data['Has Online delivery'] == 'Yes']['Restaurant Name'].count()
    dine_in_count = country_data[country_data['Has Table booking'] == 'Yes']['Restaurant Name'].count()
    delivery_vs_dinein = pd.DataFrame({
        'Service': ['Online Delivery', 'Dine-in'],
        'Count': [online_delivery_count, dine_in_count]
    })
    fig = px.pie(delivery_vs_dinein, 
                names='Service', 
                values='Count', 
                title=f'Online Delivery vs Dine-in in {country}')
    st.plotly_chart(fig)

    col1,col2=st.columns(2)
    with col1:
        vote=country_data[['Votes','Restaurant Name','City']].sort_values(by='Votes', ascending=False).reset_index(drop=True).head(5)
        st.write('Restaurant with High vote', vote)

    with col2:
        vote1=country_data[['Votes','Restaurant Name','City']].sort_values(by='Votes', ascending=False).reset_index(drop=True).tail(5)
        st.write('Restaurant which has less vote', vote1)

with tab3:
    st.write("### KEY INSIGHTS:")
    st.write("### **India has the highest number of restaurants**")
    
    st.write("**RATING DISTRIBUTION:** ")
    st.write("- **0**: White - Not rated")
    st.write("  - **1.8 to 2.4**: Red - Poor")
    st.write("  - **2.5 to 3.4**: Orange - Average")
    st.write("  - **3.5 to 3.9**: Yellow - Good")
    st.write("  - **4.0 to 4.4**: Green - Very Good")
    st.write("  - **4.5 to 4.9**: Dark Green - Excellent")
    st.write("- The majority of restaurants have an **aggregate rating** in the range of **3.0 to 3.9**, indicating that most are rated as 'Good'.")
    st.write("- **Average-rated (orange) restaurants** (rating 2.5 to 3.4) are the most common.")
    st.write("- There is a high number of **unrated restaurants**, which requires further investigation.")

    st.write(" **ONLINE DELIVERY INSIGHTS**")
    st.write("- **India** and **UAE** are the only countries offering online delivery:")
    st.write("  - **India** accounts for **98.9%** of total online delivery orders.")
    st.write("  - **UAE** contributes **1.14%**.")

    st.write(" **TABLE BOOKING INSIGHTS**")
    st.write("- **Table booking** is popular in:")
    st.write("  - **India**: 95.9% of table bookings.")
    st.write("  - **UAE**: 1.55% of table bookings.")
    st.write("  - **Philippines**: 1.21% of table bookings.")
    st.write("- Other countries where table booking is preferred include **United Kingdom**, **South Africa**, and **Qatar**.")

    st.write("### **INDIA ANALYSIS**")
    st.write("- **Top Rated Restaurants**: The highest-rated restaurants in the dataset include **AN's-Absolute Barbecues**, **Naturals Ice Cream**, and **Zolocrust - Hotel Clarks Amer**, with aggregate ratings of 4.9 and above.")
    st.write("- **Most expensive restaurants**: The most expensive restaurants based on the 'Average Cost for Two' are **Orient Express - Taj Palace Hotel**, **Tian - Asian Cuisine Studio - ITC Maurya**, and **Bukhara - ITC Maurya**, with average costs of Rs. 8000, Rs. 7000, and Rs. 6500 for two people, respectively.")
    st.write("- **Most expensive cuisines**: The most expensive cuisines based on the 'Average Cost for Two' are **European**, **Asian (Japanese, Korean, Thai, Chinese)**, and **North Indian**, with average costs of Rs. 8000, Rs. 7000, and Rs. 6500 for two people, respectively.")
    st.write("- **Least Expensive Cuisines**: The least expensive cuisines are **Chinese, North Indian, Fast Food**, **Cafe, Italian, Mexican, North Indian, Continental**, **Street Food**, and **Cafe, North Indian, Chinese**, with average costs starting from Rs. 0 for two people.")
    st.write(" - **Customer Preferences:** In India, **68.6%** of customers prefer **online delivery** while **31.4%** prefer **table bookings** ")
    st.write(" - **Voting Insights:** **Top 3 highest-voted restaurants** are **Toit**, **Truffles**, and **Hauz Khas Social** and the **Least voted restaurants** are **TAG**, **Urban Patty House**, and **Rasoi - The Indian Zaika**.")

    st.write("**LIVING COSTS IN CITIES**")
    st.write("- **High living costs**: **Panchkula**, **Hyderabad**, and **Pune** with average costs for two at Rs. 2000, Rs. 1131.11, and Rs. 1337.50 respectively.")
    st.write("- **Low living costs**: **Varanasi**, **Amritsar**, and **Faridabad** with average costs for two at Rs. 505, Rs. 480.95, and Rs. 447.61 respectively.")

    st.write("**SPENDING PATTERNS IN INDIA**")
    st.write("- **Online delivery** is most popular in **Pune**, **Hyderabad**, and **Bangalore**.")
    st.write("- **Table bookings (dine-in)** are most popular in **Ghaziabad**, **New Delhi**, and **Gurgaon**.")

    st.write("**LOCATION INSIGHTS**")
    st.write("- To explore specific **cities** or **countries**, select the location from the dropdown menu for detailed insights like top rated restaurants, famous cuisines, costly Restaurants, costly cuisines , online delivery vs table booking and Restaurants with high vote & less vote.")
