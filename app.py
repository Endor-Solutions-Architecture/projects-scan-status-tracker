import os
from utils import fetch_auth_token, fetch_all_projects, fetch_latest_scan_result
import streamlit as st
import pandas as pd

#######################################################
# Fetch ENV
#######################################################
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
api_host = os.getenv('API_HOST')
namespace = os.getenv('API_NAMESPACE')
auth_url = api_host + "/v1/auth/api-key"
auth_params = { "key" : api_key, "secret" : api_secret}

#######################################################
# Streamlit app
#######################################################

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Set Page Title
st.markdown(f"<h1 style='color: green;'>Projects Scan Status Tracker For {namespace.upper()}</h1>",unsafe_allow_html=True)

# Cache the fetch_auth_token function
@st.cache_data
def fetch_cached_auth_token(auth_url,auth_params):
    return fetch_auth_token(auth_url,auth_params)

# Cache the fetch_cached_projects function
@st.cache_data
def fetch_cached_projects(api_host,namespace,token):
    return fetch_all_projects(api_host,namespace,token)

# Cache the fetch_cached_latest_scan_result function
@st.cache_data
def fetch_cached_latest_scan_result(api_host,namespace,project_uuid,token):
    return fetch_latest_scan_result(api_host,namespace,project_uuid,token)


if api_key or api_secret:
    token = fetch_cached_auth_token(auth_url,auth_params)
    if token == None:
        st.write("Token Expired!!!")
else:
    token = os.getenv('API_TOKEN')
if token:
  projects = fetch_cached_projects(api_host,namespace,token)
  projects_status_list = []
  for project in projects:
    latest_scan_status = fetch_cached_latest_scan_result(api_host,namespace,project["project_uuid"],token)
    project_url = "https://app.endorlabs.com/t/"+namespace+"/projects/"+project["project_uuid"]
    projects_status_dictionary = { "project_name" : project["project_name"], "project_url" : project_url, "project_status" : latest_scan_status }
    projects_status_list.append(projects_status_dictionary)

# Convert data to DataFrame
  df = pd.DataFrame(projects_status_list)
  project_status_options = ["SEE ALL"] + df['project_status'].unique().tolist()
  selected_project_status = st.selectbox('Filter Projects By Latest Scan Status', project_status_options)
  
  if selected_project_status == "SEE ALL":
    st.dataframe(df)
  else:
    selected_data = df[df['project_status'] == selected_project_status]
    st.dataframe(selected_data)

# Option to clear or reload the cache
if st.button("Clear Cache and Rerun"):
    st.cache_data.clear()
    st.rerun()