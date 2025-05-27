from time import sleep
import requests
import json
from utils.helper import get_snyk_token

SNYK_TOKEN = get_snyk_token()

rest_headers = {'Content-Type': 'application/vnd.api+json', 'Authorization': f'token {SNYK_TOKEN}'}
v1Headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'token {SNYK_TOKEN}'}
rest_version = '2024-10-15'           

# Return all Snyk orgs in group
def get_snyk_orgs(groupId, region):
    print(f"Collecting snyk organization data for {groupId}")
    url = f'https://{region}/rest/groups/{groupId}/orgs?version={rest_version}&limit=10'
    has_next_link = True
    data = []
    while has_next_link:
        try:
            orgs_response = requests.get(url, headers=rest_headers)
            orgs_data = orgs_response.json()['data']
            data.extend(orgs_data)
            if orgs_response.status_code == 429:
                print(f"Rate limit exceeded. Waiting for 60 seconds.")
                sleep(61)
                continue
            try:
                url = f'https://{region}' + orgs_response.json()['links']['next']
            except:
                has_next_link = False
                return data
        except requests.RequestException as e:
            print(f"Error getting orgs for group {groupId}: {e}")
            return []

# Get targets from all Snyk Orgs by source type.
def get_snyk_targets_by_type(org_id, target_type, region):
    print(f"Collecting snyk targets for organization id: {org_id} by type {target_type}")
    url = f'https://{region}/rest/orgs/{org_id}/targets?version={rest_version}&limit=100&source_types={target_type}&exclude_empty=false'
    has_next_link = True
    targets_data = []
    while has_next_link:
        try:
            targets_response = requests.get(url, headers=rest_headers)
            targets_json = targets_response.json()
            if 'data' in targets_json:
                targets_data.extend(targets_json['data'])
            else:
                targets_data.extend(targets_json)
            if targets_response.status_code == 429:
                print(f"Rate limit exceeded. Waiting for 60 seconds.")
                sleep(61)
                continue
            if 'next' in targets_json.get('links', {}):
                url = f'https://{region}' + targets_json['links']['next']
            else:
                has_next_link = False
                return targets_data
        except requests.RequestException as e:
            print(f"Error getting targets for {org_id} by type {target_type}: {e}")
            return []


# Deletes a Snyk project
def delete_snyk_target(org_id, target_id, region):
    print(f"Deleting Snyk target.  Target ID: {target_id}")
    url = f'https://{region}/rest/orgs/{org_id}/targets/{target_id}?version={rest_version}'
    retry_count = 0
    while retry_count < 3: 
        try:
            delete_target_response = requests.delete(url, headers=v1Headers, data={})
            if delete_target_response.status_code == 204:
                print("Target successfully deleted.")
                return
            if delete_target_response.status_code == 429:
                print("Rate limit exceeded. Waiting for 60 seconds.")
                sleep(61)
                retry_count += 1
                continue
            else:
                print(f"Delete target endpoint failed with status code: {delete_target_response.status_code}. Response: {delete_target_response.text}")
                return
        except Exception as e:
            print(f"Error occurred while deleting target: {str(e)}")
            retry_count += 1
            if retry_count < 3:
                print("Retrying...")
                sleep(61)
            else:
                print("Max retries reached. Giving up.")
                return 