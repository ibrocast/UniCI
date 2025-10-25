"""
UniCI Jenkins Tab
GUI for triggering and monitoring Jenkins jobs.
"""
import customtkinter as ctk

class JenkinsTab:
    """
    Encapsulates the GUI and logic for the Jenkins tab.
    """
    def __init__(self, parent_tab, main_view):
        self.parent = parent_tab
        self.main_view = main_view
        self.controller = None

        # Configure grid
        self.parent.grid_columnconfigure(0, weight=1)

        # --- Job Trigger Frame ---
        self.trigger_frame = ctk.CTkFrame(self.parent)
        self.trigger_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.trigger_frame.grid_columnconfigure(1, weight=1)

        self.job_label = ctk.CTkLabel(self.trigger_frame, text="Jenkins Job Name:")
        self.job_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.job_entry = ctk.CTkEntry(self.trigger_frame, width=300)
        self.job_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.trigger_button = ctk.CTkButton(self.trigger_frame, text="Trigger Build", command=self.on_trigger_build)
        self.trigger_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # --- Placeholder for future features ---
        self.status_frame = ctk.CTkFrame(self.parent)
        self.status_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.status_frame, text="Build status will appear in the console log below.")
        self.status_label.pack(padx=10, pady=10)

    def set_controller(self, controller):
        """Set the controller for this tab."""
        self.controller = controller

    def on_trigger_build(self):
        """Handle the trigger build button click."""
        job_name = self.job_entry.get()
        if self.controller and job_name:
            self.controller.handle_jenkins_trigger(job_name)
        elif not job_name:
            self.main_view.log_to_console("Please enter a Jenkins Job Name.", "WARN")
