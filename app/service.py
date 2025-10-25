"""
Service Layer (Model)

Handles all external API communication.
It knows nothing about the GUI or the Controller.
"""

import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, Optional

class ApiService:
    """
    Handles all API calls to Jenkins, GitHub, and GitLab.
    This class is completely decoupled from the GUI.
    """
    def __init__(self):
        # Configuration will be stored here
        self.github_token: Optional[str] = None
        self.gitlab_url: Optional[str] = None
        self.gitlab_token: Optional[str] = None
        self.jenkins_url: Optional[str] = None
        self.jenkins_user: Optional[str] = None
        self.jenkins_token: Optional[str] = None

    def update_config(self, config_data: Dict[str, str]):
        """Updates the API credentials from the settings panel."""
        self.github_token = config_data.get("github_token")
        self.gitlab_url = config_data.get("gitlab_url", "").rstrip('/')
        self.gitlab_token = config_data.get("gitlab_token")
        self.jenkins_url = config_data.get("jenkins_url", "").rstrip('/')
        self.jenkins_user = config_data.get("jenkins_user")
        self.jenkins_token = config_data.get("jenkins_token")

    def get_github_branches(self, repo_name: str) -> Dict[str, Any]:
        """
        Fetches branches for a GitHub repository (e.g., 'owner/repo').
        """
        if not self.github_token:
            raise ValueError("GitHub token is not set.")
        if not repo_name:
            raise ValueError("Repository name is required.")

        url = f"https://api.github.com/repos/{repo_name}/branches"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()

    def trigger_gitlab_pipeline(self, project_id: str, ref: str) -> Dict[str, Any]:
        """
        Triggers a new pipeline for a GitLab project on a specific ref (branch/tag).
        """
        if not self.gitlab_url or not self.gitlab_token:
            raise ValueError("GitLab URL or token is not set.")
        if not project_id:
            raise ValueError("Project ID is required.")
        if not ref:
            raise ValueError("Branch/Ref is required.")

        url = f"{self.gitlab_url}/api/v4/projects/{project_id}/pipeline"
        headers = {"PRIVATE-TOKEN": self.gitlab_token}
        data = {"ref": ref}

        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return response.json()

    def trigger_jenkins_build(self, job_name: str) -> str:
        """
        Triggers a build for a Jenkins job.
        Uses /build for simple jobs. Use /buildWithParameters for parameterized jobs.
        """
        if not self.jenkins_url or not self.jenkins_user or not self.jenkins_token:
            raise ValueError("Jenkins URL, user, or token is not set.")
        if not job_name:
            raise ValueError("Job name is required.")

        # Note: This triggers a build *without* parameters.
        # For parameters, change URL to /buildWithParameters and send form data
        url = f"{self.jenkins_url}/job/{job_name.strip()}/build"
        auth = HTTPBasicAuth(self.jenkins_user, self.jenkins_token)

        # Jenkins requires a CSRF token (crumb) for POST requests
        crumb_url = f"{self.jenkins_url}/crumbIssuer/api/json"
        try:
            crumb_response = requests.get(crumb_url, auth=auth, timeout=5)
            crumb_response.raise_for_status()
            crumb_data = crumb_response.json()
            crumb_header = {crumb_data["crumbRequestField"]: crumb_data["crumb"]}
        except Exception as e:
            # Fallback if crumbs are disabled or request fails
            print(f"Could not get Jenkins crumb, proceeding without it... Error: {e}")
            crumb_header = {}

        response = requests.post(url, auth=auth, headers=crumb_header, timeout=10)

        # Successful build trigger returns 201 (Created)
        if response.status_code == 201:
            return f"Build successfully triggered for {job_name}."
        else:
            raise Exception(f"Failed to trigger build. Status: {response.status_code}, Text: {response.text}")