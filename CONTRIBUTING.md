Contributing to UniCI

We are thrilled that you are interested in contributing to UniCI! Your help is valuable in making this tool better for everyone.

This document outlines the guidelines for contributing to the project, including how to submit bug reports, request features, and make code contributions.

Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct (To be created, but for now, please be respectful and constructive). By participating, you are expected to uphold this code.

How Can I Contribute?

Reporting Bugs

If you find a bug, please ensure it hasn't already been reported by searching the Issues on GitHub.

If you can't find an existing issue, please open a new one. Be sure to include:

A clear and descriptive title.

A step-by-step description of how to reproduce the bug.

The expected behavior vs. the actual behavior.

Your Operating System (e.g., Windows 11, macOS Sonoma).

Any screenshots that might be helpful.

Any error messages from the application's console log.

Suggesting Enhancements

We are open to new ideas! If you have a suggestion for a new feature or an improvement to an existing one:

Search the Issues to see if the feature has already been requested.

If not, open a new issue to start a discussion. Please provide as much context as possible about the "what" and "why" of your suggestion.

Pull Request (PR) Process

We actively welcome your code contributions!

Fork the repository to your own GitHub account.

Create a new branch for your feature or fix:

git checkout -b feature/my-awesome-feature


or

git checkout -b fix/my-bug-fix


Make your changes. Please adhere to the project's architecture:

GUI changes go in app/view.py or app/view_tabs/.

State management or logic goes in app/controller.py.

API communication goes in app/service.py.

Test your changes to ensure they work as expected and don't break existing functionality.

Commit your changes with a clear and descriptive commit message:

git commit -m "feat: Add GitHub PR approval button"


Push your branch to your fork:

git push origin feature/my-awesome-feature


Open a Pull Request from your fork's branch to the main branch of the original UniCI repository.

Describe your changes in the PR description, linking to any relevant issues (e.g., "Closes #42").

Your PR will be reviewed by a maintainer, who may suggest changes. We appreciate your patience and collaboration during this process!

Thank you for your contribution!