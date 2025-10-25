"""
UniCI GitLab Tab
GUI for triggering and monitoring GitLab pipelines.
"""
import customtkinter as ctk

class GitLabTab:
    """
    Encapsulates the GUI and logic for the GitLab tab.
    """
    def __init__(self, parent_tab, main_view):
        self.parent = parent_tab
        self.main_view = main_view
        self.controller = None

        # Configure grid
        self.parent.grid_columnconfigure(0, weight=1)

        # --- Pipeline Trigger Frame ---
        self.trigger_frame = ctk.CTkFrame(self.parent)
        self.trigger_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.trigger_frame.grid_columnconfigure(1, weight=1)

        self.project_id_label = ctk.CTkLabel(self.trigger_frame, text="GitLab Project ID:")
        self.project_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.project_id_entry = ctk.CTkEntry(self.trigger_frame, width=200)
        self.project_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.ref_label = ctk.CTkLabel(self.trigger_frame, text="Branch/Ref:")
        self.ref_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.ref_entry = ctk.CTkEntry(self.trigger_frame, width=200)
        self.ref_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.trigger_button = ctk.CTkButton(self.trigger_frame, text="Trigger Pipeline", command=self.on_trigger_pipeline)
        self.trigger_button.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="e")

        # --- Placeholder for future features ---
        self.status_frame = ctk.CTkFrame(self.parent)
        self.status_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.status_frame, text="Pipeline status will appear in the console log below.")
        self.status_label.pack(padx=10, pady=10)

    def set_controller(self, controller):
        """Set the controller for this tab."""
        self.controller = controller

    def on_trigger_pipeline(self):
        """Handle the trigger pipeline button click."""
        project_id = self.project_id_entry.get()
        ref = self.ref_entry.get()

        if self.controller and project_id and ref:
            self.controller.handle_gitlab_trigger(project_id, ref)
        else:
            self.main_view.log_to_console("Please enter a Project ID and Branch/Ref.", "WARN")