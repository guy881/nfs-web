from fabric.api import env
from fabtools import git


def pull():
    git.pull(env.project_dir)


def reload():
    pull()
