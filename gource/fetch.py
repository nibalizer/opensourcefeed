#!/usr/bin/env python3
"""Creates gource videos from CNCF devstats projects"""

import os
import subprocess
import yaml

import requests


def get_project_list(url):
    """Grabs a projects.yaml, filters appropriately, returns a project list"""
    projects = yaml.load(requests.get(url).text)
    repos = []
    for project in projects['projects']:
        # if graduated
        if projects['projects'][project]['status'] == "Graduated":
            repos.append(projects['projects'][project]['main_repo'])
    return list(filter(None, repos))  # remove the projects with no repo


def clone(project):
    """Clones (or pulls) a project"""
    repo_name = project.split("/")[1]
    if not os.path.exists(project.split("/")[1]):
        print("%s not found at %s, cloning" % (project, repo_name))
        # TODO: implement
        subprocess.run(["git", "clone", "https://github.com/" + project, "git/" + repo_name])
    else:
        print("%s found at %s, pulling" % (project, repo_name))
        # TODO: implement


def grab_avatars(project):
    """Grabs the avatars for a projects, puts them in $PROJECT/.git/avatars"""
    repo_name = project.split("/")[1]
    if os.path.exists("{}/.git/avatars".format(repo_name)):
        print("Avatars found at {}/.git/avatars, not updating")
        # TODO: implement
    else:
        print("No avatars found at expected location: %s/.git/avatars"
              % (repo_name))
        # TODO: implement


def run_gource(project):
    """Runs a gource/ffmpeg pipeline to generate the desired video"""
    print("Generating output, command: gource ... | ffmpeg %s" % project)
    # TODO: implement


def main():
    """Main control loop"""
    projects = get_project_list("https://raw.githubusercontent.com" +
                                "/cncf/devstats/master/projects.yaml")

    for project in projects:
        clone(project)
        grab_avatars(project)
        run_gource(project)
    for project in projects:
        if not os.path.exists(project.split("/")[1]):
            print("%s not found, cloning" % project)
        else:
            print("%s directory found, pulling" % project)
        # Clone/pull
        # Grab avatars (if avatar dir doesn't exist)
        # Run gource/ffmpeg transcoding command
    print(projects)


if __name__ == "__main__":
    main()
