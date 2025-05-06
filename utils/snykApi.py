from time import sleep
import requests
import json
from utils.helper import get_snyk_token

SNYK_TOKEN = get_snyk_token()

rest_headers = {'Content-Type': 'application/vnd.api+json', 'Authorization': f'token {SNYK_TOKEN}'}
v1Headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'token {SNYK_TOKEN}'}
rest_version = '2024-10-15'
    
                

# Return all Snyk orgs in group
def get_snyk_orgs(groupId):
    print(f"Collecting snyk organization targets for {groupId}")
    url = f'https://api.snyk.io/rest/groups/{groupId}/orgs?version={rest_version}&limit=100'
    has_next_link = True
    orgs_data = []
    while has_next_link:
        try:
            orgs_response = requests.get(url, headers=rest_headers)
            orgs_data = orgs_response.json()['data']
            orgs_data.extend(orgs_data)
            if orgs_response.status_code == 429:
                print(f"Rate limit exceeded. Waiting for 60 seconds.")
                sleep(61)
                continue
            if 'next' in orgs_response.json()['links']:
                url = 'https://api.snyk.io' + orgs_response.json()['links']['next']
            else:
                has_next_link = False
                return orgs_data
        except requests.RequestException as e:
            print(f"Error getting orgs for group {groupId}: {e}")
            return []

# Get cpp projects from all Snyk Orgs.
def get_snyk_projects_by_type(org_id, project_type):
    print(f"Collecting snyk projects for organization id: {org_id} by type {project_type}")
    url = f'https://api.snyk.io/rest/orgs/{org_id}/projects?version={rest_version}&limit=100&origins={project_type}'
    has_next_link = True
    projects_data = []
    while has_next_link:
        try:
            projects_response = requests.get(url, headers=rest_headers)
            response_json = projects_response.json()
            print(json.dumps(response_json, indent=4))
            if 'data' in response_json:
                projects_data.extend(response_json['data'])
            else:
                projects_data.extend(response_json)
            if projects_response.status_code == 429:
                print(f"Rate limit exceeded. Waiting for 60 seconds.")
                sleep(61)
                continue
            if 'next' in response_json.get('links', {}):
                url = 'https://api.snyk.io' + response_json['links']['next']
            else:
                has_next_link = False
                return projects_data
        except requests.RequestException as e:
            print(f"Error getting projects for {org_id} by type {project_type}: {e}")
            return []


# Deletes a Snyk project
def delete_snyk_project(org_id, project_id):
    print(f"Deleting Snyk project.  Project ID: {project_id}")
    url = f'https://api.snyk.io/v1/org/{org_id}/project/{project_id}'
        
    try:
        delete_project_response = requests.delete(url, headers=v1Headers, data={})
        if delete_project_response.status_code == 200:
            print("Project successfully deleted.")    
    except:
        print(f"Delete project endpoint failed with the following error code: {delete_project_response.status_code}.  Here is the error: {delete_project_response} ") 