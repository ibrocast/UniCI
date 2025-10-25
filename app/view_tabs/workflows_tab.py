"""
UniCI Workflows Tab
GUI for configuring and running multi-step "macro" workflows.
(This is a placeholder implementation)
"""
import customtkinter as ctk

class WorkflowsTab:
    """
    Encapsulates the GUI and logic for the Workflows tab.
    """
    def __init__(self, parent_tab, main_view):
        self.parent = parent_tab
        self.main_view = main_view
        self.controller = None

        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)

        # --- Placeholder Frame ---
        self.placeholder_frame = ctk.CTkFrame(self.parent)
        self.placeholder_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.placeholder_label = ctk.CTkLabel(
            self.placeholder_frame,
            text="Feature Coming Soon: Workflow Macros",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.placeholder_label.pack(pady=(50, 10))

        self.placeholder_desc = ctk.CTkLabel(
            self.placeholder_frame,
            text="This tab will allow you to chain multiple actions together into a single button.\n\n"
                 "Example: 'Promote to Staging'\n"
                 "1. Trigger Jenkins Build\n"
                 "2. Monitor Build Status\n"
                 "3. If Success, Trigger Jenkins Deploy\n"
                 "4. Post 'Success' to Slack",
            justify="left",
            text_color="gray"
        )
        self.placeholder_desc.pack(pady=10, padx=20)

    def set_controller(self, controller):
        """Set the controller for this tab."""
        self.controller = controller

    def on_run_workflow(self):
        """Placeholder for a workflow button."""
        if self.controller:
            self.main_view.log_to_console("Workflow execution not yet implemented.", "WARN")