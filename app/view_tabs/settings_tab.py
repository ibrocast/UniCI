"""
UniCI Settings Tab
GUI for configuring all service credentials and URLs.
Uses 'keyring' for secure credential storage.
"""
import customtkinter as ctk

class SettingsTab:
    """
    Encapsulates the GUI and logic for the Settings tab.
    """
    def __init__(self, parent_tab, main_view):
        self.parent = parent_tab
        self.main_view = main_view
        self.controller = None

        # Configure grid
        self.parent.grid_columnconfigure(1, weight=1)

        # --- Jenkins Settings ---
        self.jenkins_label = ctk.CTkLabel(self.parent, text="Jenkins", font=ctk.CTkFont(size=16, weight="bold"))
        self.jenkins_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        self.jenkins_url_label = ctk.CTkLabel(self.parent, text="Jenkins URL:")
        self.jenkins_url_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.jenkins_url_entry = ctk.CTkEntry(self.parent, width=400)
        self.jenkins_url_entry.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        self.jenkins_user_label = ctk.CTkLabel(self.parent, text="Jenkins User:")
        self.jenkins_user_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.jenkins_user_entry = ctk.CTkEntry(self.parent, width=400)
        self.jenkins_user_entry.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        self.jenkins_token_label = ctk.CTkLabel(self.parent, text="Jenkins API Token:")
        self.jenkins_token_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.jenkins_token_entry = ctk.CTkEntry(self.parent, width=400, show="*")
        self.jenkins_token_entry.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        # --- GitHub Settings ---
        self.github_label = ctk.CTkLabel(self.parent, text="GitHub", font=ctk.CTkFont(size=16, weight="bold"))
        self.github_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        self.github_token_label = ctk.CTkLabel(self.parent, text="GitHub PAT:")
        self.github_token_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        self.github_token_entry = ctk.CTkEntry(self.parent, width=400, show="*")
        self.github_token_entry.grid(row=5, column=1, padx=20, pady=5, sticky="ew")

        # --- GitLab Settings ---
        self.gitlab_label = ctk.CTkLabel(self.parent, text="GitLab", font=ctk.CTkFont(size=16, weight="bold"))
        self.gitlab_label.grid(row=6, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        self.gitlab_url_label = ctk.CTkLabel(self.parent, text="GitLab URL:")
        self.gitlab_url_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        self.gitlab_url_entry = ctk.CTkEntry(self.parent, width=400)
        self.gitlab_url_entry.grid(row=7, column=1, padx=20, pady=5, sticky="ew")

        self.gitlab_token_label = ctk.CTkLabel(self.parent, text="GitLab Token:")
        self.gitlab_token_label.grid(row=8, column=0, padx=20, pady=5, sticky="w")
        self.gitlab_token_entry = ctk.CTkEntry(self.parent, width=400, show="*")
        self.gitlab_token_entry.grid(row=8, column=1, padx=20, pady=5, sticky="ew")

        # --- Save Button ---
        self.save_button = ctk.CTkButton(self.parent, text="Save Configuration", command=self.save_settings)
        self.save_button.grid(row=9, column=1, padx=20, pady=20, sticky="e")

    def set_controller(self, controller):
        """Set the controller and load initial data."""
        self.controller = controller
        self.load_settings()

    def load_settings(self):
        """Load settings from config and keyring."""
        # Load non-sensitive URLs
        self.jenkins_url_entry.insert(0, self.controller.get_config_setting("jenkins_url", ""))
        self.jenkins_user_entry.insert(0, self.controller.get_config_setting("jenkins_user", ""))
        self.gitlab_url_entry.insert(0, self.controller.get_config_setting("gitlab_url", "https://gitlab.com"))

        # Load sensitive tokens from keyring
        # We put placeholder text if a token is found, but don't display the token
        jenkins_user = self.controller.get_config_setting("jenkins_user", "")
        if jenkins_user and self.controller.get_credential("UniCI_Jenkins", jenkins_user):
            self.jenkins_token_entry.insert(0, "********")

        if self.controller.get_credential("UniCI_GitHub", "github_token"):
            self.github_token_entry.insert(0, "********")

        if self.controller.get_credential("UniCI_GitLab", "gitlab_token"):
            self.gitlab_token_entry.insert(0, "********")

    def save_settings(self):
        """Save all settings to config or keyring."""
        if not self.controller:
            return

        try:
            # Save non-sensitive config
            self.controller.set_config_setting("jenkins_url", self.jenkins_url_entry.get())
            self.controller.set_config_setting("jenkins_user", self.jenkins_user_entry.get())
            self.controller.set_config_setting("gitlab_url", self.gitlab_url_entry.get())

            # Save sensitive tokens to keyring
            # Only update the token if the user entered something new (not the placeholder)
            jenkins_token = self.jenkins_token_entry.get()
            if jenkins_token and jenkins_token != "********":
                self.controller.set_credential("UniCI_Jenkins", self.jenkins_user_entry.get(), jenkins_token)
                self.jenkins_token_entry.delete(0, "end")
                self.jenkins_token_entry.insert(0, "********") # Replace with placeholder

            github_token = self.github_token_entry.get()
            if github_token and github_token != "********":
                self.controller.set_credential("UniCI_GitHub", "github_token", github_token)
                self.github_token_entry.delete(0, "end")
                self.github_token_entry.insert(0, "********")

            gitlab_token = self.gitlab_token_entry.get()
            if gitlab_token and gitlab_token != "********":
                self.controller.set_credential("UniCI_GitLab", "gitlab_token", gitlab_token)
                self.gitlab_token_entry.delete(0, "end")
                self.gitlab_token_entry.insert(0, "********")

            self.main_view.log_to_console("Configuration saved successfully.", "SUCCESS")
        except Exception as e:
            self.main_view.log_to_console(f"Error saving settings: {e}", "ERROR")