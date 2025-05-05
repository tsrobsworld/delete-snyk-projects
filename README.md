# Snyk Delete Projects

This repository contains a CLI tool for deleting projects from Snyk based on the integration type.

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

## Example

To delete projects from a Snyk organization or group, use the `delete_projects` function

```bash
python index.py --help

python index.py <snyk_id> <group_or_organization> <snyk_integration_type> --dry-run
```
    


