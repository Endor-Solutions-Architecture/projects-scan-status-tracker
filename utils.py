import requests
import json

def fetch_auth_token(auth_url,auth_params):
  """Fetches data from a URL, parses the JSON response, and returns the token value.

  Args: 
    auth_url: The URL endpoint to fetch the auth token from
    auth_params: Json which includes api key and secret

  Returns:
    The token value from the JSON response, or None if an error occurred or "token" key is not found.
  """

  try:
    response = requests.post(auth_url, json = auth_params)
    response.raise_for_status()  # Raise exception for non-2xx status codes

    # Parse JSON response
    data = response.json()
    return data.get("token")  # Use get() to avoid KeyError if "token" is missing

  except requests.exceptions.RequestException as e:
    print(f"Error parsing JSON data or 'token' key not found: {e}")
    return None
  except (json.JSONDecodeError, KeyError) as e:
    print(f"Error parsing JSON data or 'token' key not found: {e}")
    return None

def fetch_all_projects(api_host,namespace,token):
  """Fetches data from a URL, parses the JSON response, and returns the dictionary of projects.

  Args: 
    api_host: Host URL to run the API against
    namespace: Tenant namespace to run the API against
    token: Auth Token to access the projects API

  Returns:
    The dictionary of projects within the given namespace
  """

  projects_dictionary = []
  project_url = api_host + "/v1/namespaces/" + namespace + "/projects"
  auth_header = "Bearer " + token
  headers = { "Authorization" : auth_header}
  response =  requests.get(project_url, headers=headers)
  projects = response.json()["list"]["objects"]
  for project in projects:
    try:
      project_name = project["spec"]["git"]["full_name"]
      project_uuid = project["uuid"]
      project_data = { "project_name":project_name, "project_uuid" : project_uuid }
      projects_dictionary.append(project_data)
    except KeyError:
      continue
  return projects_dictionary

def fetch_latest_scan_result(api_host,namespace,project_uuid,token):
  """Fetches data from a URL, parses the JSON response, and returns the latest scan result.

  Args:
    api_host: Host URL to run the API against
    namespace: Tenant namespace to run the API against
    project_uuid: UUID of the project to fetch dependencies from
    token: Auth Token to access the projects API

  Returns:
    The latest scan result for the given project
  """
  query_params = "list_parameters.filter=meta.parent_uuid==" +  project_uuid + "&list_parameters.sort.path=meta.create_time&list_parameters.sort.order=SORT_ENTRY_ORDER_DESC"
  scan_results_url = api_host + "/v1/namespaces/" + namespace + "/scan-results"
  auth_header = "Bearer " + token
  headers = { "Authorization" : auth_header}
  response =  requests.get(scan_results_url, params = query_params, headers=headers)
  try:
    latest_scan_result = response.json()["list"]["objects"][0]
    return latest_scan_result["spec"]["status"]
  except IndexError:
    return "RESCAN_REQUIRED"
