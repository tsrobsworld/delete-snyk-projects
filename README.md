# Snyk Delete Targets and Projects

This repository contains a CLI tool for deleting targets and projects from Snyk based on the integration type.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tsrobsworld/delete-snyk-projects.git
   ```

2. Navigate to the project directory:
   ```bash
   cd delete-snyk-projects
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the utilities, you need to have a valid Snyk token. Ensure that your environment is set up to provide SNYK_TOKEN environment variable.

### Command Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `snyk_id` | Required Argument | - | The Snyk ID of the group or organization to delete projects for |
| `group_or_organization` | Required Argument | - | Specify group or organization level to delete projects. Options: 'group', 'organization', 'org' |
| `snyk_integration_type` | Required Argument | - | Specify the integration type to delete projects for. Examples: 'github', 'github-enterprise', 'gitlab', 'azure-repos', 'bitbucket-server', 'bitbucket-cloud', 'cli' |
| `--dry-run` | Flag | False | Perform a dry run without actually deleting projects |
| `--region` | String | 'api.us.snyk.io' | Specify the region to delete projects for. Examples: 'api.snyk.io', 'api.us.snyk.io', 'api.eu.snyk.io', 'api.au.snyk.io' |
| `--debug` | Flag | False | Enable debug mode to show detailed project information |

## Example

To delete projects from a Snyk organization or group, use the following command:

```bash
# Show help
python index.py --help

# Dry run example
python index.py <snyk_id> <group_or_organization> <snyk_integration_type> --dry-run

# Debug mode example
python index.py <snyk_id> <group_or_organization> <snyk_integration_type> --debug

# Full example with all options
python index.py <snyk_id> <group_or_organization> <snyk_integration_type> --dry-run --region api.us.snyk.io --debug
```
    


