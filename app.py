import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="NPI Search", page_icon="", layout="centered", initial_sidebar_state="expanded")

# Input field for search terms
search_term = st.text_input("Physician Name:")

# Function to retrieve results from API
def get_results(fname,lname):
    # Replace 'API_URL' with the actual API endpoint
    response = requests.get(f"https://npiregistry.cms.hhs.gov/api/?number=&enumeration_type=&taxonomy_description=&name_purpose=&first_name={fname}&use_first_name_alias=&last_name={lname}&organization_name=&address_purpose=&city=&state=&postal_code=&country_code=&limit=&skip=&pretty=&version=2.1")
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve results")
        return []

# Display results in a table
fname = ''
lname = ''

if search_term:
    fname = search_term.split()[0]
    if len(search_term.split()) > 1:
        lname = search_term.split()[1]
    # todo: parse 
    # city = 

    results = get_results(fname, lname)
    #st.write(len(results))
    if results['results']:
        #df = pd.DataFrame(results)
        df = pd.json_normalize(results['results'])
                          #, "address", "city", "state", "postal_code", "country_code"]])
        df1 = df[["basic.first_name", "basic.last_name", "basic.credential", "number", "addresses", "taxonomies"]]
        df1['city'] = df['addresses'].apply(lambda x: x[0]['city'])
        df1['state'] = df['addresses'].apply(lambda x: x[0]['state'])
        st.dataframe(df1.drop(columns=['addresses', 'taxonomies']))
    else:
        st.write("No results found")
