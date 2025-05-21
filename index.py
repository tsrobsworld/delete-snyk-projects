import typer
import json
from utils.snykApi import get_snyk_orgs, get_snyk_projects_by_type, delete_snyk_project
app = typer.Typer()

def delete_projects(snyk_id, group_or_organization, snyk_integration_type, dry_run, region, debug):
    project_id_list = []
    if group_or_organization.lower() == "group":
        snyk_orgs = get_snyk_orgs(snyk_id, region)
        for org in snyk_orgs:
            project_data = get_snyk_projects_by_type(org['id'], snyk_integration_type, region)
            if debug:
                print(f"Project data for org: {org['id']}")
                print(json.dumps(project_data, indent=4))
            for project in project_data:
                project_id_list.append({
                    'project_id': project['id'],
                    'org_id': project['relationships']['organization']['data']['id']
                })

    if group_or_organization.lower() == "organization" or group_or_organization.lower() == "org":
        project_data = get_snyk_projects_by_type(snyk_id, snyk_integration_type, region)
        for project in project_data:
            if debug:
                print(f"Project data for org: {snyk_id}")
                print(json.dumps(project, indent=4))
            project_id_list.append({
                'project_id': project['id'],
                'org_id': project['relationships']['organization']['data']['id']
            })
    print(type(dry_run))
    if dry_run:
        print(json.dumps(project_id_list, indent=4))
        print(f"Dry run complete. Would have deleted {len(project_id_list)} projects.")
    else:
        for project in project_id_list:
            print(f"Deleting Project ID: {project['project_id']} from Org ID: {project['org_id']}")
            if debug:
                print(json.dumps(project, indent=4))
            delete_snyk_project(project['org_id'], project['project_id'], region)

@app.command()
def delete_projects_for_integration_type(
    snyk_id: str = typer.Argument(..., help="The Snyk ID of the group or organization to delete projects for"),
    group_or_organization: str = typer.Argument(..., help="Specify group or organization level to delete projects.  Example: 'group', 'organization', org"),
    snyk_integration_type: str = typer.Argument(..., help="Specify the integration type to delete projects for.  Example: 'github, github-enterprise, gitlab, azure-repos, bitbucket-server, bitbucket-cloud, cli, etc'"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Dry run the deletion of projects.  Example: --dry-run"),
    region: str = typer.Option('api.us.snyk.io', "--region", help="Specify the region to delete projects for.  Example: 'api.snyk.io, api.us.snyk.io, api.eu.snyk.io, api.au.snyk.io'"),
    debug: bool = typer.Option(False, "--debug", help="Debug the deletion of projects.  Example: --debug")
):
    """
    Deletes projects based on the provided Snyk ID, group or organization level, and integration type.
    """
    print(f"Deleting projects in the Snyk organization ID: {snyk_id}, "
          f"At the level of: {group_or_organization}, "
          f"With the integration type: {snyk_integration_type}")
    if group_or_organization.lower() == "group" or group_or_organization.lower() == "organization" or group_or_organization.lower() == "org":
        delete_projects(snyk_id, group_or_organization, snyk_integration_type, dry_run, region, debug)
    else:
        print("Invalid group or organization level. Please specify 'group', 'organization', or 'org'.")
        typer.Exit(1)
    
    

if __name__ == "__main__":
    app()
