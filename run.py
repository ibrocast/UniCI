"""
Main Entry Point for the CI/CD Utility

This file initializes and runs the main application.
"""

import customtkinter as ctk
from app.view import App  # Import the main App class from our package

# --- Main execution ---
if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Options: "blue", "green","dark-blue"

    app = App()
    app.mainloop()
