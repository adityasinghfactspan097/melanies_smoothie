# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col,when_matched
# Write directly to the app
st.title(" MY PARENTS NEW HEALTHY DINER")
st.write(
    """Choose the fruits you want in your custumazied smothie!
    """
)



name_of_order = st.text_input('Name of Smoothies: ')
st.write('Name of Smoothies will be: ', name_of_order)

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list=st.multiselect(
'Choose upto 5 ingredients',
my_dataframe,
max_selections=6
)


if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_of_order + """')"""



time_to_insert=st.button('Submit order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    
    st.success('your Smoothie is orderd!', icon='✅')

fruityvice_response = requests.get("https://world.openfoodfacts.org/api/v3/product/737628064502.json")

fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

