import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Function to execute MySQL query
def execute_query(query):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

# Function to create a Plotly bar chart
def create_bar_chart(df, x, y, title, x_title, y_title):
    fig = px.bar(df, x=x, y=y, title=title, labels={x: x_title, y: y_title})
    st.plotly_chart(fig)

# Window 1: Total population of each District
def window_1():
    query = "SELECT District, Population FROM test.Census_df"
    df = pd.DataFrame(execute_query(query), columns=['District', 'Population'])
    district_population = df.groupby('District')['Population'].sum().reset_index()
    create_bar_chart(district_population, 'District', 'Population', 'Total Population of Each District', 'District', 'Population')

# Window 2: Literate male and female in each district
def window_2():
    query = "SELECT District, Literate_Male, Literate_Female FROM test.Census_df"
    df = pd.DataFrame(execute_query(query), columns=['District', 'Literate_Male', 'Literate_Female'])
    df_melted = df.melt(id_vars='District', value_vars=['Literate_Male', 'Literate_Female'], var_name='Gender', value_name='Count')
    create_bar_chart(df_melted, 'District', 'Count', 'Literate Male and Female in Each District', 'District', 'Count')

# Window 3: Percentage of workers in each district
def window_3():
    query = "SELECT District, ROUND((Workers/Population)*100, 2) AS Percentage_of_Workers FROM test.Census_df"
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['District', 'Percentage_of_Workers'])
    create_bar_chart(df, 'District', 'Percentage_of_Workers', 'Percentage of Workers in Each District', 'District', 'Percentage of Workers')

# Window 4: Households with LPG or PNG as Cooking fuel
def window_4():
    query = "SELECT District, LPG_or_PNG_Households FROM test.Census_df"
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['District', 'LPG_or_PNG_Households'])
    create_bar_chart(df, 'District', 'LPG_or_PNG_Households', 'Households with LPG or PNG as Cooking Fuel', 'District', 'LPG or PNG Households')

# Window 5: Religious composition of each district
def window_5():
    query = """
        SELECT District, 
                ROUND((Hindus/Population)*100, 2) AS Hindus, 
                ROUND((Muslims/Population)*100, 2) AS Muslims, 
                ROUND((Christians/Population)*100, 2) AS Christians, 
                ROUND((Sikhs/Population)*100, 2) AS Sikhs, 
                ROUND((Buddhists/Population)*100, 2) AS Buddhists, 
                ROUND((Jains/Population)*100, 2) AS Jains, 
                ROUND((Others_Religions/Population)*100, 2) AS Other_Religions, 
                ROUND((Religion_Not_Stated/Population)*100, 2) AS Religion_Not_Stated 
        FROM test.Census_df
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['District', 'Hindus', 'Muslims', 'Christians', 'Sikhs', 'Buddhists', 'Jains', 'Other_Religions', 'Religion_Not_Stated'])
    df_melted = df.melt(id_vars='District', value_vars=['Hindus', 'Muslims', 'Christians', 'Sikhs', 'Buddhists', 'Jains', 'Other_Religions', 'Religion_Not_Stated'], var_name='Religion', value_name='Percentage')
    create_bar_chart(df_melted, 'District', 'Percentage', 'Religious Composition of Each District', 'District', 'Percentage')

def window_6():
    query = "SELECT District, Households_with_Internet FROM test.Census_df"
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['District', 'Households_with_Internet'])
    create_bar_chart(df, 'District', 'Households_with_Internet', 'Households with Internet in Each District', 'District', 'Households with Internet')

# Window 7: Educational attainment distribution in each district
def window_7():
    query = """
        SELECT District, Below_Primary_Education, Primary_Education, Middle_Education, 
                Secondary_Education, Higher_Education, Graduate_Education, Other_Education 
        FROM test.Census_df
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['District', 'Below_Primary_Education', 'Primary_Education', 'Middle_Education', 
                                        'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education'])
    df_melted = df.melt(id_vars='District', value_vars=['Below_Primary_Education', 'Primary_Education', 'Middle_Education', 
                                                        'Secondary_Education', 'Higher_Education', 'Graduate_Education', 'Other_Education'],
                        var_name='Education_Level', value_name='Count')
    create_bar_chart(df_melted, 'District', 'Count', 'Educational Attainment Distribution in Each District', 'District', 'Count')

# Window 8: Households with access to various modes of transports in each district
def window_8():
    query = """
        SELECT District, Households_with_Bicycle, Households_with_Car_Jeep_Van, 
                Households_with_Radio_Transistor, Households_with_Scooter_Motorcycle_Moped 
        FROM test.Census_df
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['District', 'Households_with_Bicycle', 'Households_with_Car_Jeep_Van', 
                                        'Households_with_Radio_Transistor', 'Households_with_Scooter_Motorcycle_Moped'])
    df_melted = df.melt(id_vars='District', value_vars=['Households_with_Bicycle', 'Households_with_Car_Jeep_Van', 
                                                        'Households_with_Radio_Transistor', 'Households_with_Scooter_Motorcycle_Moped'],
                        var_name='Transport_Mode', value_name='Count')
    create_bar_chart(df_melted, 'District', 'Count', 'Households with Access to Various Modes of Transport', 'District', 'Count')

# Window 9: Condition of occupied census houses
def window_9():
    query = """
        SELECT District, 
                Condition_of_occupied_census_houses_Dilapidated_Households AS Occupied_Dilapidated_Houses, 
                Households_with_separate_kitchen_Cooking_inside_house AS Houses_with_seperate_Kitchen, 
                Having_bathing_facility_Total_Households AS Houses_with_Bathing_facility, 
                Having_latrine_facility_within_the_premises_Total_Households AS Houses_with_Latrine_facility, 
                Not_having_bathing_facility_within_the_premises_Total_Households AS Houses_without_Bathing_facility, 
                Not_having_latrine_within_premises_Other_source_Open_Households AS Houses_without_latrine_facility 
        FROM test.Census_df
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['District', 'Occupied_Dilapidated_Houses', 'Houses_with_seperate_Kitchen', 
                                        'Houses_with_Bathing_facility', 'Houses_with_Latrine_facility', 
                                        'Houses_without_Bathing_facility', 'Houses_without_latrine_facility'])
    df_melted = df.melt(id_vars='District', value_vars=['Occupied_Dilapidated_Houses', 'Houses_with_seperate_Kitchen', 
                                                        'Houses_with_Bathing_facility', 'Houses_with_Latrine_facility', 
                                                        'Houses_without_Bathing_facility', 'Houses_without_latrine_facility'],
                        var_name='Condition', value_name='Count')
    create_bar_chart(df_melted, 'District', 'Count', 'Condition of Occupied Census Houses', 'District', 'Count')

# Window 10: Household size distribution in each district
def window_10():
    query = """
        SELECT District, Household_size_1_person_Households AS 1_Person, 
                Household_size_2_persons_Households AS 2_Persons, 
                Household_size_3_persons_Households AS 3_Persons, 
                Household_size_4_persons_Households AS 4_Persons, 
                Household_size_5_persons_Households AS 5_Persons, 
                Household_size_6_8_persons_Households AS 6_to_8_Persons, 
                Household_size_9_persons_and_above_Households AS More_than_9_Persons 
        FROM test.Census_df
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['District', '1_Person', '2_Persons', '3_Persons', '4_Persons', '5_Persons', '6_to_8_Persons', 'More_than_9_Persons'])
    df_melted = df.melt(id_vars='District', value_vars=['1_Person', '2_Persons', '3_Persons', '4_Persons', '5_Persons', '6_to_8_Persons', 'More_than_9_Persons'],
                        var_name='Household_Size', value_name='Count')
    create_bar_chart(df_melted, 'District', 'Count', 'Household Size Distribution in Each District', 'District', 'Count')

# Window 11: Total number of households in each state
def window_11():
    query = "SELECT state_UT, SUM(Households) AS Total_Households FROM test.Census_df GROUP BY state_UT"
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Total_Households'])
    create_bar_chart(df, 'state_UT', 'Total_Households', 'Total Number of Households in Each State', 'State', 'Total Households')

# Window 12: Households with latrine facility within the premises in each state
def window_12():
    query = """
        SELECT state_UT, SUM(Having_latrine_facility_within_the_premises_Total_Households) AS Households_with_Latrine 
        FROM test.Census_df 
        GROUP BY state_UT
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Households_with_Latrine'])
    create_bar_chart(df, 'state_UT', 'Households_with_Latrine', 'Households with Latrine Facility in Each State', 'State', 'Households with Latrine')

# Window 13: Average household size in each state
def window_13():
    query = """
        SELECT state_UT, ROUND(AVG(Household_size_1_person_Households), 2) AS Avg_1_Person, 
                ROUND(AVG(Household_size_2_persons_Households), 2) AS Avg_2_Persons, 
                ROUND(AVG(Household_size_3_persons_Households), 2) AS Avg_3_Persons, 
                ROUND(AVG(Household_size_4_persons_Households), 2) AS Avg_4_Persons, 
                ROUND(AVG(Household_size_5_persons_Households), 2) AS Avg_5_Persons, 
                ROUND(AVG(Household_size_6_8_persons_Households), 2) AS Avg_6_to_8_Persons, 
                ROUND(AVG(Household_size_9_persons_and_above_Households), 2) AS Avg_More_than_9_Persons 
        FROM test.Census_df 
        GROUP BY state_UT
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Avg_1_Person', 'Avg_2_Persons', 'Avg_3_Persons', 'Avg_4_Persons', 'Avg_5_Persons', 'Avg_6_to_8_Persons', 'Avg_More_than_9_Persons'])
    df_melted = df.melt(id_vars='state_UT', value_vars=['Avg_1_Person', 'Avg_2_Persons', 'Avg_3_Persons', 'Avg_4_Persons', 'Avg_5_Persons', 'Avg_6_to_8_Persons', 'Avg_More_than_9_Persons'],
                        var_name='Household_Size', value_name='Average')
    create_bar_chart(df_melted, 'state_UT', 'Average', 'Average Household Size in Each State', 'State', 'Average Household Size')

# Window 14: Owned versus rented houses in each state
def window_14():
    query = """
        SELECT state_UT, SUM(Ownership_Owned_Households) AS Owned_Houses, SUM(Ownership_Rented_Households) AS Rented_Houses 
        FROM test.Census_df 
        GROUP BY state_UT
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Owned_Houses', 'Rented_Houses'])
    df_melted = df.melt(id_vars='state_UT', value_vars=['Owned_Houses', 'Rented_Houses'], var_name='Ownership', value_name='Count')
    create_bar_chart(df_melted, 'state_UT', 'Count', 'Owned vs Rented Houses in Each State', 'State', 'Count')

# Window 15: Distribution of different types of latrine facilities in each state
def window_15():
    query = """
        SELECT state_UT, SUM(Type_of_latrine_facility_Pit_latrine_Households) AS Pit_Latrine, 
        SUM(Type_of_latrine_facility_Night_soil_disposed_into_open_drain) AS Night_soil_disposed_into_open_drain_Latrine, 
        SUM(Type_of_latrine_Flush_pour_connected_to_other_system_Households) AS Flush_or_Pour_Latrine, 
        SUM(Type_of_latrine_facility_Other_latrine_Households) AS Other_Latrine_types 
        FROM test.Census_df 
        GROUP BY state_UT
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Pit_Latrine', 'Night_soil_disposed_into_open_drain_Latrine', 'Flush_or_Pour_Latrine', 'Other_Latrine_types'])
    df_melted = df.melt(id_vars='state_UT', value_vars=['Pit_Latrine', 'Night_soil_disposed_into_open_drain_Latrine', 'Flush_or_Pour_Latrine', 'Other_Latrine_types'], var_name='Latrine_Type', value_name='Count')
    create_bar_chart(df_melted, 'state_UT', 'Count', 'Distribution of Latrine Facilities in Each State', 'State', 'Count')

# Window 16: Households with drinking water sources near the premises in each state
def window_16():
    query = """
        SELECT state_UT, SUM(Location_of_drinking_water_source_Near_the_premises_Households) AS Households_with_drinking_water_source_Near_the_premises 
        FROM test.Census_df 
        GROUP BY state_UT
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Households_with_drinking_water_source_Near_the_premises'])
    create_bar_chart(df, 'state_UT', 'Households_with_drinking_water_source_Near_the_premises', 'Households with Drinking Water Sources Near the Premises in Each State', 'State', 'Households with Drinking Water Source')

# Window 17: Average household income distribution in each state based on power parity categories
def window_17():
    query = """
        SELECT state_UT, 
        ROUND(AVG(Power_Parity_Less_than_Rs_45000), 2) AS Avg_Power_Parity_Less_than_Rs_45000, 
        ROUND(AVG(Power_Parity_Rs_45000_90000), 2) AS Avg_Power_Parity_Rs_45000_90000, 
        ROUND(AVG(Power_Parity_Rs_90000_150000), 2) AS Avg_Power_Parity_Rs_90000_150000, 
        ROUND(AVG(Power_Parity_Rs_45000_150000), 2) AS Avg_Power_Parity_Rs_45000_150000, 
        ROUND(AVG(Power_Parity_Rs_150000_240000), 2) AS Avg_Power_Parity_Rs_150000_240000, 
        ROUND(AVG(Power_Parity_Rs_240000_330000), 2) AS Avg_Power_Parity_Rs_240000_330000, 
        ROUND(AVG(Power_Parity_Rs_150000_330000), 2) AS Avg_Power_Parity_Rs_150000_330000, 
        ROUND(AVG(Power_Parity_Rs_330000_425000), 2) AS Avg_Power_Parity_Rs_330000_425000, 
        ROUND(AVG(Power_Parity_Rs_425000_545000), 2) AS Avg_Power_Parity_Rs_425000_545000, 
        ROUND(AVG(Power_Parity_Rs_330000_545000), 2) AS Avg_Power_Parity_Rs_330000_545000, 
        ROUND(AVG(Power_Parity_Above_Rs_545000), 2) AS Avg_Power_Parity_Above_Rs_545000 
        FROM test.Census_df 
        GROUP BY state_UT
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Avg_Power_Parity_Less_than_Rs_45000', 'Avg_Power_Parity_Rs_45000_90000', 'Avg_Power_Parity_Rs_90000_150000', 'Avg_Power_Parity_Rs_45000_150000', 'Avg_Power_Parity_Rs_150000_240000', 'Avg_Power_Parity_Rs_240000_330000', 'Avg_Power_Parity_Rs_150000_330000', 'Avg_Power_Parity_Rs_330000_425000', 'Avg_Power_Parity_Rs_425000_545000', 'Avg_Power_Parity_Rs_330000_545000', 'Avg_Power_Parity_Above_Rs_545000'])
    df_melted = df.melt(id_vars='state_UT', value_vars=['Avg_Power_Parity_Less_than_Rs_45000', 'Avg_Power_Parity_Rs_45000_90000', 'Avg_Power_Parity_Rs_90000_150000', 'Avg_Power_Parity_Rs_45000_150000', 'Avg_Power_Parity_Rs_150000_240000', 'Avg_Power_Parity_Rs_240000_330000', 'Avg_Power_Parity_Rs_150000_330000', 'Avg_Power_Parity_Rs_330000_425000', 'Avg_Power_Parity_Rs_425000_545000', 'Avg_Power_Parity_Rs_330000_545000', 'Avg_Power_Parity_Above_Rs_545000'], var_name='Income_Category', value_name='Average')
    create_bar_chart(df_melted, 'state_UT', 'Average', 'Average Household Income Distribution in Each State', 'State', 'Average Income')

# Window 18: Percentage of married couples with different household sizes in each state
def window_18():
    query = """
        SELECT state_UT, 
        ROUND(SUM(Married_couples_1_Households)/SUM(Population) * 100, 2) AS Percentage_of_Married_couples_1_Households, 
        ROUND(SUM(Married_couples_2_Households)/SUM(Population) * 100, 2) AS Percentage_of_Married_couples_2_Households, 
        ROUND(SUM(Married_couples_3_Households)/SUM(Population) * 100, 2) AS Percentage_of_Married_couples_3_Households, 
        ROUND(SUM(Married_couples_3_or_more_Households)/SUM(Population) * 100, 2) AS Percentage_of_Married_couples_3_or_more_Households, 
        ROUND(SUM(Married_couples_4_Households)/SUM(Population) * 100, 2) AS Percentage_of_Married_couples_4_Households, 
        ROUND(SUM(Married_couples_5__Households)/SUM(Population) * 100, 2) AS Percentage_of_Married_couples_5__Households, 
        ROUND(SUM(MarMarried_couples_None_Households)/SUM(Population) * 100, 2) AS Percentage_of_Married_couples_None_Households 
        FROM test.Census_df 
        GROUP BY state_UT
        """
    
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Percentage_of_Married_couples_1_Households', 'Percentage_of_Married_couples_2_Households', 'Percentage_of_Married_couples_3_Households', 'Percentage_of_Married_couples_3_or_more_Households', 'Percentage_of_Married_couples_4_Households', 'Percentage_of_Married_couples_5__Households', 'Percentage_of_Married_couples_None_Households'])
    df_melted = df.melt(id_vars='state_UT', value_vars=['Percentage_of_Married_couples_1_Households', 'Percentage_of_Married_couples_2_Households', 'Percentage_of_Married_couples_3_Households', 'Percentage_of_Married_couples_3_or_more_Households', 'Percentage_of_Married_couples_4_Households', 'Percentage_of_Married_couples_5__Households', 'Percentage_of_Married_couples_None_Households'], var_name='Household_Size', value_name='Percentage')
    create_bar_chart(df_melted, 'state_UT', 'Percentage', 'Percentage of Married Couples with Different Household Sizes in Each State', 'State', 'Percentage')

def window_19():
    query = """
        SELECT state_UT, SUM(Power_Parity_Less_than_Rs_45000) AS Households_below_poverty_line
        FROM test.Census_df
        GROUP BY state_UT
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['state_UT', 'Households_below_poverty_line'])
    create_bar_chart(df, 'state_UT', 'Households_below_poverty_line', 'Households below the Poverty Line in Each State', 'State', 'Households Below Poverty Line')

# Window 20: Overall Literacy Rate of Each State
def window_20():
    query = """
        SELECT State_UT, ROUND(SUM(Literate)/SUM(Population) * 100, 2) AS Percentage_of_Literacy
        FROM test.Census_df
        GROUP BY state_UT
    """
    result = execute_query(query)
    df = pd.DataFrame(result, columns=['State_UT', 'Percentage_of_Literacy'])
    create_bar_chart(df, 'State_UT', 'Percentage_of_Literacy', 'Overall Literacy Rate of Each State', 'State', 'Percentage of Literacy')    
        
# Add other window functions similarly...

# Dropdown selection for windows
def main():
    st.title('Census Data Visualization')

    window_options = {
        'Total Population of Each District': window_1,
        'Literate Male and Female in Each District': window_2,
        'Percentage of Workers in Each District': window_3,
        'Households with LPG or PNG as Cooking Fuel': window_4,
        'Religious Composition of Each District': window_5,
        'Educational Attainment Distribution in Each District': window_7,
        'Households with Access to Various Modes of Transport': window_8,
        'Condition of Occupied Census Houses': window_9,
        'Household Size Distribution in Each District': window_10,
        'Total Number of Households in Each State': window_11,
        'Households with Latrine Facility in Each State': window_12,
        'Average Household Size in Each State': window_13,
        'Owned versus Rented Houses in Each State': window_14,
        'Distribution of Latrine Facilities in Each State': window_15,
        'Households with Drinking Water Sources Near the Premises in Each State': window_16,
        'Average Household Income Distribution in Each State': window_17,
        'Percentage of Married Couples with Different Household Sizes in Each State': window_18,
        'Households below the Poverty Line in Each State': window_19,
        'Overall Literacy Rate of Each State': window_20,
        
    }

    window_selection = st.selectbox('Select Query Window', list(window_options.keys()))

    # Execute the selected window function
    if window_selection:
        window_options[window_selection]()

if __name__ == "__main__":
    main()