"""
View Layer

Handles all GUI creation and user interaction.
It only calls methods on the AppController.
"""

import customtkinter as ctk
import queue
from app.controller import AppController # Import from our package

class App(ctk.CTk):
    """
    The main application GUI class (View).
    It is responsible for building the UI and forwarding user events
    to the AppController.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Cross-Platform CI/CD Utility")
        self.geometry("900x700")

        # Create the thread-safe queue and the controller
        self.gui_queue = queue.Queue()
        self.controller = AppController(self.gui_queue)

        # Configure main grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create TabView
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="nsew")

        self.tab_view.add("Settings")
        self.tab_view.add("Jenkins")
        self.tab_view.add("GitHub")
        self.tab_view.add("GitLab")

        # Create Console
        self.console_textbox = ctk.CTkTextbox(self, height=150, state="disabled")
        self.console_textbox.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.log_to_console("Welcome to the CI/CD Utility. Configure your services in Settings.")

        # Populate tabs
        self.create_settings_tab()
        self.create_jenkins_tab()
        self.create_github_tab()
        self.create_gitlab_tab()

        # Start the queue checker
        self.after(100, self.check_gui_queue)

    def check_gui_queue(self):
        """
        Checks the queue for new messages from the controller/threads
        and posts them to the console. Runs on the main GUI thread.
        """
        try:
            while True:
                message = self.gui_queue.get_nowait()
                self.log_to_console(message)
        except queue.Empty:
            pass  # No new messages
        finally:
            # Reschedule itself to run again
            self.after(100, self.check_gui_queue)

    def log_to_console(self, message: str):
        """Appends a message to the console text box."""
        self.console_textbox.configure(state="normal")
        self.console_textbox.insert("end", f"{message}\n")
        self.console_textbox.configure(state="disabled")
        self.console_textbox.see("end")  # Auto-scroll

    def create_settings_tab(self):
        """Creates the widgets for the 'Settings' tab."""
        tab = self.tab_view.tab("Settings")
        tab.grid_columnconfigure(1, weight=1)

        frame = ctk.CTkFrame(tab)
        frame.pack(pady=20, padx=20, fill="x")
        frame.grid_columnconfigure(1, weight=1)

        # --- Jenkins Settings ---
        ctk.CTkLabel(frame, text="Jenkins URL", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.jenkins_url_entry = ctk.CTkEntry(frame, placeholder_text="http://my-jenkins.com:8080")
        self.jenkins_url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="Jenkins User", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.jenkins_user_entry = ctk.CTkEntry(frame, placeholder_text="username")
        self.jenkins_user_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="Jenkins Token", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.jenkins_token_entry = ctk.CTkEntry(frame, placeholder_text="API Token", show="*")
        self.jenkins_token_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # --- GitHub Settings ---
        ctk.CTkLabel(frame, text="GitHub Token", anchor="w").grid(row=3, column=0, padx=10, pady=(15, 5), sticky="w")
        self.github_token_entry = ctk.CTkEntry(frame, placeholder_text="Personal Access Token", show="*")
        self.github_token_entry.grid(row=3, column=1, padx=10, pady=(15, 5), sticky="ew")

        # --- GitLab Settings ---
        ctk.CTkLabel(frame, text="GitLab URL", anchor="w").grid(row=4, column=0, padx=10, pady=(15, 5), sticky="w")
        self.gitlab_url_entry = ctk.CTkEntry(frame, placeholder_text="https://gitlab.com")
        self.gitlab_url_entry.grid(row=4, column=1, padx=10, pady=(15, 5), sticky="ew")

        ctk.CTkLabel(frame, text="GitLab Token", anchor="w").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.gitlab_token_entry = ctk.CTkEntry(frame, placeholder_text="Personal Access Token", show="*")
        self.gitlab_token_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # --- Save Button ---
        save_button = ctk.CTkButton(tab, text="Save Configuration", command=self.save_config)
        save_button.pack(pady=20)

    def save_config(self):
        """
Atts        Called by the 'Save' button.
        It collects data from entry widgets and passes it to the controller.
        """
        config_data = {
            "jenkins_url": self.jenkins_url_entry.get(),
            "jenkins_user": self.jenkins_user_entry.get(),
            "jenkins_token": self.jenkins_token_entry.get(),
            "github_token": self.github_token_entry.get(),
            "gitlab_url": self.gitlab_url_entry.get(),
            "gitlab_token": self.gitlab_token_entry.get(),
        }
        # The View only calls the controller, it doesn't save anything itself
        self.controller.update_api_config(config_data)

    def create_jenkins_tab(self):
        """Creates the widgets for the 'Jenkins' tab."""
        tab = self.tab_view.tab("Jenkins")
        tab.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(tab)
        frame.pack(pady=20, padx=20, fill="x")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Job Name", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.jenkins_job_entry = ctk.CTkEntry(frame, placeholder_text="my-pipeline-job")
        self.jenkins_job_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        trigger_button = ctk.CTkButton(frame, text="Trigger Build", command=self.trigger_jenkins_build)
        trigger_button.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

    def trigger_jenkins_build(self):
        """Passes the user action to the controller."""
        job_name = self.jenkins_job_entry.get()
        self.controller.handle_jenkins_build(job_name)

    def create_github_tab(self):
        """Creates the widgets for the 'GitHub' tab."""
        tab = self.tab_view.tab("GitHub")
        tab.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(tab)
        frame.pack(pady=20, padx=20, fill="x")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Repo Name", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.github_repo_entry = ctk.CTkEntry(frame, placeholder_text="owner/repository-name")
        self.github_repo_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        trigger_button = ctk.CTkButton(frame, text="List Branches", command=self.list_github_branches)
        trigger_button.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

    def list_github_branches(self):
        """Passes the user action to the controller."""
        repo_name = self.github_repo_entry.get()
        self.controller.handle_github_list_branches(repo_name)

    def create_gitlab_tab(self):
        """Creates the widgets for the 'GitLab' tab."""
        tab = self.tab_view.tab("GitLab")
        tab.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(tab)
        frame.pack(pady=20, padx=20, fill="x")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Project ID", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.gitlab_project_entry = ctk.CTkEntry(frame, placeholder_text="12345")
        self.gitlab_project_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(frame, text="Branch / Ref", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.gitlab_ref_entry = ctk.CTkEntry(frame, placeholder_text="main")
        self.gitlab_ref_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        trigger_button = ctk.CTkButton(frame, text="Trigger Pipeline", command=self.trigger_gitlab_pipeline)
        trigger_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    def trigger_gitlab_pipeline(self):
        """Passes the user action to the controller."""
        project_id = self.gitlab_project_entry.get()
        ref = self.gitlab_ref_entry.get()
        self.controller.handle_gitlab_trigger_pipeline(project_id, ref)