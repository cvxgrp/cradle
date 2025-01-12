#    Copyright 2025 Stanford University Convex Optimization Group
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import re

import questionary


def _validate_project_name(project_name):
    if not re.match(r"^[a-z][a-z0-9_]+$", project_name):
        raise ValueError(
            "Project name must start with a lowercase letter, "
            "followed by one or more lowercase letters, digits, or underscores."
        )
    return project_name


def _validate_username(username):
    if not username:
        raise ValueError("Username cannot be empty.")
    return username


def _validate_description(description):
    if not description:
        raise ValueError("Description cannot be empty.")
    return description


def _validate_status(status):
    if status not in ["public", "private", "internal"]:
        raise ValueError("Status must be one of: public, private, or internal.")
    return status


def ask():
    # Get user inputs with questionary
    project_name = questionary.text("Enter your project name:").ask()
    project_name = _validate_project_name(project_name.lower())

    username = questionary.text("Enter your GitHub username (e.g., 'cvxgrp'):").ask() or "tschm"
    username = _validate_username(username)

    description = questionary.text("Enter a brief description of your project:").ask() or "Some computations"
    description = _validate_description(description)

    status = questionary.select(
        "What is the visibility status of the repository?", choices=["public", "private", "internal"], default="public"
    ).ask()
    status = _validate_status(status)

    # Generate dynamic values
    repo_name = project_name.lower()
    repository_url = f"https://github.com/{username}/{repo_name}"
    ssh_uri = f"git@github.com:{username}/{repo_name}.git"
    gh_create = f"gh repo create {username}/{repo_name} --{status} --description '{description}'"

    # Display the results
    print("\n--- Repository Details ---")
    print(f"Project Name: {repo_name}")
    print(f"GitHub Username: {username}")
    print(f"Description: {description}")
    print(f"Visibility: {status}")
    print(f"Repository URL: {repository_url}")
    print(f"SSH URI: {ssh_uri}")
    print(f"Command to create the repo: {gh_create}")

    context = {
        "project_name": project_name.lower(),
        "username": username,
        "description": description,
        "status": status,
        "ssh_uri": ssh_uri,
        "repository_url": repository_url,
        "command": gh_create,
    }

    return context
