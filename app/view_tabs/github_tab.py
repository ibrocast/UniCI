"""
UniCI GitHub Tab
GUI for interacting with GitHub, e.g., viewing Pull Requests.
"""
import customtkinter as ctk

class GitHubTab:
    """
    Encapsulates the GUI and logic for the GitHub tab.
    """
    def __init__(self, parent_tab, main_view):
        self.parent = parent_tab
        self.main_view = main_view
        self.controller = None
        self.pr_data_cache = [] # To store full PR data

        # Configure grid
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)

        # --- Repo Frame ---
        self.repo_frame = ctk.CTkFrame(self.parent)
        self.repo_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.repo_frame.grid_columnconfigure(1, weight=1)

        self.repo_label = ctk.CTkLabel(self.repo_frame, text="GitHub Repo (owner/name):")
        self.repo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.repo_entry = ctk.CTkEntry(self.repo_frame, width=300)
        self.repo_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.refresh_button = ctk.CTkButton(self.repo_frame, text="Refresh PRs", command=self.on_refresh_prs)
        self.refresh_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # --- PR List Frame ---
        self.pr_frame = ctk.CTkScrollableFrame(self.parent, label_text="Open Pull Requests")
        self.pr_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.pr_frame.grid_columnconfigure(0, weight=1)

        # This widget will be populated by display_pull_requests
        self.no_prs_label = ctk.CTkLabel(self.pr_frame, text="Refresh to see pull requests.")
        self.no_prs_label.grid(row=0, column=0, padx=10, pady=10)

    def set_controller(self, controller):
        """Set the controller and load initial data."""
        self.controller = controller
        # Load last used repo from config
        self.repo_entry.insert(0, self.controller.get_config_setting("github_repo", ""))

    def on_refresh_prs(self):
        """Handle the refresh PRs button click."""
        repo_name = self.repo_entry.get()
        if self.controller and repo_name:
            self.controller.handle_github_refresh_prs(repo_name)
            # Clear current view
            for widget in self.pr_frame.winfo_children():
                widget.destroy()
            self.loading_label = ctk.CTkLabel(self.pr_frame, text="Loading...")
            self.loading_label.grid(row=0, column=0, padx=10, pady=10)
        elif not repo_name:
            self.main_view.log_to_console("Please enter a GitHub Repo Name.", "WARN")

    def display_pull_requests(self, pr_list):
        """
        Called by the controller to populate the scrollable frame with PRs.
        This method MUST run on the main GUI thread.
        """
        # Clear "Loading..." or old PRs
        for widget in self.pr_frame.winfo_children():
            widget.destroy()

        self.pr_data_cache = pr_list

        if not pr_list:
            self.no_prs_label = ctk.CTkLabel(self.pr_frame, text="No open pull requests found.")
            self.no_prs_label.grid(row=0, column=0, padx=10, pady=10)
            return

        for i, pr in enumerate(pr_list):
            pr_frame = ctk.CTkFrame(self.pr_frame, fg_color=("gray85", "gray17"))
            pr_frame.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
            pr_frame.grid_columnconfigure(1, weight=1)

            title = f"#{pr['number']}: {pr['title']}"
            author = pr['user']['login']
            pr_info = f"by @{author}  |  {pr['head']['ref']} -> {pr['base']['ref']}"

            title_label = ctk.CTkLabel(pr_frame, text=title, font=ctk.CTkFont(weight="bold"), anchor="w")
            title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(5,0), sticky="w")

            info_label = ctk.CTkLabel(pr_frame, text=pr_info, text_color="gray", anchor="w")
            info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,5), sticky="w")

            approve_button = ctk.CTkButton(
                pr_frame,
                text="Approve",
                width=80,
                command=lambda p=pr: self.on_approve_pr(p)
            )
            approve_button.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="e")

    def on_approve_pr(self, pr_data):
        """Handle the approve button click for a specific PR."""
        if self.controller:
            self.controller.handle_github_approve_pr(pr_data)
