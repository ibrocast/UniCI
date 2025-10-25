"""
Controller Layer

Manages application logic, state, and threading.
Connects the View (App) to the Service (ApiService).
"""

import threading
import queue
from typing import Dict, Any, Optional
from app.service import ApiService  # Import from our package

class AppController:
    """
    Acts as the intermediary between the GUI (View) and the API (Service).
    Handles user actions from the GUI and dispatches them to the ApiService
    in background threads.
    """
    def __init__(self, gui_queue: queue.Queue):
        self.api_service = ApiService()
        self.gui_queue = gui_queue  # Thread-safe queue to log to the GUI

    def log_to_gui(self, message: str):
        """Safely puts a log message into the GUI's update queue."""
        self.gui_queue.put(message)

    def run_in_thread(self, target_func, *args):
        """
        Helper function to run a given function in a daemon thread.
        This prevents the GUI from freezing during network requests.
        """
        thread = threading.Thread(target=target_func, args=args, daemon=True)
        thread.start()

    def update_api_config(self, config_data: Dict[str, str]):
        """Public method called by the GUI to update config."""
        try:
            self.api_service.update_config(config_data)
            self.log_to_gui("Configuration saved successfully.")
        except Exception as e:
            self.log_to_gui(f"Error saving config: {e}")

    # --- Jenkins Handlers ---

    def handle_jenkins_build(self, job_name: str):
        """Public method called by GUI. Runs the worker in a thread."""
        self.log_to_gui(f"Attempting to trigger Jenkins job: {job_name}...")
        self.run_in_thread(self._jenkins_build_worker, job_name)

    def _jenkins_build_worker(self, job_name: str):
        """Worker function that runs in a thread."""
        try:
            result_message = self.api_service.trigger_jenkins_build(job_name)
            self.log_to_gui(f"Jenkins Success: {result_message}")
        except Exception as e:
            self.log_to_gui(f"Jenkins Error: {e}")

    # --- GitHub Handlers ---

    def handle_github_list_branches(self, repo_name: str):
        """Public method called by GUI."""
        self.log_to_gui(f"Attempting to fetch branches for: {repo_name}...")
        self.run_in_thread(self._github_list_branches_worker, repo_name)

    def _github_list_branches_worker(self, repo_name: str):
        """Worker function that runs in a thread."""
        try:
            branches = self.api_service.get_github_branches(repo_name)
            branch_names = [branch['name'] for branch in branches]
            self.log_to_gui(f"GitHub Success: Found {len(branch_names)} branches.")
            self.log_to_gui(f"Branches: {', '.join(branch_names)}")
        except Exception as e:
            self.log_to_gui(f"GitHub Error: {e}")

    # --- GitLab Handlers ---

    def handle_gitlab_trigger_pipeline(self, project_id: str, ref: str):
        """Public method called by GUI."""
        self.log_to_gui(f"Attempting to trigger pipeline for project {project_id} on ref {ref}...")
        self.run_in_thread(self._gitlab_trigger_pipeline_worker, project_id, ref)

    def _gitlab_trigger_pipeline_worker(self, project_id: str, ref: str):
        """Worker function that runs in a thread."""
        try:
            response = self.api_service.trigger_gitlab_pipeline(project_id, ref)
            self.log_to_gui(f"GitLab Success: Pipeline created.")
            self.log_to_gui(f"  ID: {response.get('id')}, Status: {response.get('status')}")
            self.log_to_gui(f"  Web URL: {response.get('web_url')}")
        except Exception as e:
            self.log_to_gui(f"GitLab Error: {e}")