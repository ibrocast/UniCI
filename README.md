UniCI - The Unified CI/CD Dashboard

UniCI is a cross-platform desktop application designed to be a "single pane of glass" for all your development and CI/CD operations. It provides a unified interface to trigger, monitor, and manage workflows across Jenkins, GitHub, and GitLab.

No more juggling browser tabs.

Download

Get the latest official release here:
https://github.com/ibrocast/UniCI/releases/tag/v1.0.0

The Problem

As developers, we constantly switch contexts:

We write code in our IDE.

We push to GitHub and create a Pull Request.

We go to Jenkins to trigger a build for that PR.

We wait, staring at the Jenkins "blue ball" animation.

If it fails, we dig through console logs.

If it succeeds, we go to GitLab to trigger the deployment pipeline.

We wait again.

UniCI is built to consolidate this entire workflow into a single, responsive application.

Core Features

Unified Dashboard: Control Jenkins, GitHub, and GitLab from one place.

Real-Time Build Monitoring: UniCI doesn't just "fire and forget." It triggers a build and monitors it, reporting "Running," "Success," or "Failed" statuses directly to the console.

One-Click Fixes: When a build fails, UniCI provides a direct link to the failed console log, getting you to the error in a single click.

Dynamic Parameters: Automatically detects and prompts for build parameters (for both Jenkins and GitLab).

Secure Credential Storage: Uses the native OS credential manager (keyring) to securely store your API tokens. No plain-text secrets.

Developer Hub: Go beyond CI/CD. The GitHub tab can list your open PRs, allowing you to review and approve them directly from the app.

Cross-Platform: Built with CustomTkinter, it runs natively on Windows, macOS, and Linux.

Project Structure

This project is built with a clean, 3-tier architecture to ensure strict separation of concerns, making it secure, testable, and easy to maintain.

UniCI/
├── app/
│   ├── view.py             (GUI - The main App window)
│   ├── view_tabs/        (GUI - Each tab is a separate file)
│   ├── controller.py       (Logic - The "brain" connecting GUI and services)
│   ├── service.py          (Services - All third-party API calls)
│   ├── config_manager.py   (Handles non-sensitive config.json)
│
├── run.py                  (Main entry point to start the app)
├── requirements.txt        (Dependencies)
├── README.md               (You are here!)
├── LICENSE
└── CONTRIBUTING.md


View (view.py, view_tabs/): The CustomTkinter GUI. Knows nothing about APIs. It only knows how to draw widgets and call the Controller when a button is clicked.

Controller (controller.py): The "brain." Takes requests from the View (e.g., "user clicked trigger build"), runs them in a background thread, calls the Service, and passes results back to the View's console.

Service (service.py): The "muscle." Only knows how to talk to APIs (requests). It is stateless and knows nothing about the GUI.

Getting Started

Prerequisites

Python 3.7+

pip and venv

Installation & Running

Clone the repository:

git clone [https://github.com/ibrocast/UniCI.git](https://github.com/ibrocast/UniCI.git)
cd UniCI


Create a virtual environment:

python -m venv venv


Activate it:

Windows (Git Bash): source venv/Scripts/activate

macOS/Linux: source venv/bin/activate

Install dependencies:

pip install -r requirements.txt


Run the application:

python run.py


First Run: The app will launch. Go to the Settings tab, enter your URLs and API tokens, and click Save. Your tokens will be stored securely in your OS keychain.

How to Package for Distribution (Optional)

You can package UniCI as a standalone executable for users who don't have Python installed.

Install PyInstaller:

pip install pyinstaller


Build the executable:

On Windows:

pyinstaller --onefile --windowed --name=UniCI run.py


On macOS:

pyinstaller --onefile --windowed --name=UniCI --add-data "venv/lib/python3.x/site-packages/customtkinter:customtkinter" run.py


(Note: macOS often requires the --add-data flag for CustomTkinter themes)

Your standalone application will be in the dist/ folder.

Contributing

Contributions are what make the open-source community amazing. We welcome pull requests for bug fixes, new features, or improvements to the documentation.

Please read our CONTRIBUTING.md file for details on our code of conduct and the process for submitting pull requests.

License

This project is licensed under the MIT License - see the LICENSE file for details.