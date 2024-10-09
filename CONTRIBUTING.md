# Contributing to TaskSync

We’re excited that you’re interested in contributing to TaskSync! This guide will help you understand how to contribute, from reporting bugs to suggesting new features and submitting code.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Feature Requests](#feature-requests)
   - [Submitting Pull Requests](#submitting-pull-requests)
3. [Development Guidelines](#development-guidelines)
   - [Setting Up the Environment](#setting-up-the-environment)
   - [Coding Style](#coding-style)
   - [Testing](#testing)
4. [Issue Tracker](#issue-tracker)

---

## Code of Conduct

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md) to ensure a respectful and inclusive environment for all contributors.

---

## How to Contribute

### Reporting Bugs
If you find a bug or an issue while using TaskSync, please report it by following these steps:
1. **Check the issue tracker** to see if the bug has already been reported.
2. If not, **open a new issue** and provide the following details:
   - A clear and descriptive title.
   - Steps to reproduce the issue.
   - Expected behavior vs. actual behavior.
   - Any relevant screenshots or error logs.
   - Information about your system and environment (e.g., OS, browser, Python version).

### Feature Requests
If you have a new idea or feature you’d like to see in TaskSync:
1. **Check the issue tracker** to see if the feature has already been requested.
2. If not, **open a new feature request** and include:
   - A clear and descriptive title.
   - A detailed explanation of the feature.
   - How the feature would improve TaskSync.
   - Any relevant examples, mockups, or references.

### Submitting Pull Requests
We welcome pull requests! If you’d like to submit changes, follow these steps:
1. Fork the repository and create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes. Ensure that:
   - Your code follows the style guidelines (see [Coding Style](#coding-style)).
   - You’ve included tests for any new functionality.
3. Commit your changes:
   ```bash
   git commit -m 'Add feature description'
   ```
4. Push the branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request on the main repository:
   - Clearly describe your changes.
   - Link to any relevant issues or feature requests.
   - Include any special notes for reviewers.

---

## Development Guidelines

### Setting Up the Environment
Follow these steps to set up the development environment for TaskSync:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Prideland-Okoi/tasksync-flask-backend.git
   cd tasksync-flask-backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   - Configure your `.env` file with the appropriate database settings.
   - Run migrations:
     ```bash
     flask db upgrade
     ```

4. **Run the application locally:**
   ```bash
   flask run
   ```

### Coding Style
Please adhere to the following style guidelines when contributing:
- **PEP 8**: Follow the PEP 8 guidelines for Python code.
- **Comments**: Write clear, concise comments for any non-obvious code sections.
- **Function/Variable Names**: Use descriptive names for functions and variables.
- **Docstrings**: Include docstrings for all methods and classes.

For front-end development, follow standard HTML, CSS, and JavaScript conventions.

### Testing
Before submitting a pull request, make sure all tests pass:
1. **Run existing tests:**
   ```bash
   pytest
   ```
2. **Add new tests** for any new functionality or bug fixes.
3. Ensure that your code does not introduce any new linting errors.

---

## Issue Tracker

We use GitHub’s [issue tracker](https://github.com/prideland-okoi/tasksync-flask-backend/issues) to manage bug reports and feature requests. Feel free to browse the existing issues or create new ones as described above.

---

Thank you for helping to make TaskSync better! Every contribution, no matter how small, helps improve the project. If you have any questions, feel free to reach out through an issue or discussion.
