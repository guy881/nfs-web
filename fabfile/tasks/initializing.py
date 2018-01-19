import json
import os

from fabric.api import cd, env
from fabtools import pyenv, require, uwsgi


def setup_user():
    """
    Require user belonging to www-data and sudo groups that will be in charge of
    this project on remote server (all further actions should be executed as him)
    """
    require.user(
        env.username, group="www-data", password=env.username, shell="/bin/bash"
    )
    require.sudoer(env.username)
    env.user = env.username


def setup_project():
    """
    Require working copy of project cloned from remote repository.
    """
    require.directory(
        env.project_dir, use_sudo=True, owner=env.user, group="www-data"
    )
    with cd(env.project_dir):
        require.git.working_copy(env.config["repository"], directly=True)
        require.file(
            os.path.join(
                env.project_dir, env.config["project"], "secrets.json"
            ), json.dumps(env.secrets)
        )


def setup_python():
    """
    Require proper version of python to be installed and available in special
    virtualenv.
    """
    require.pyenv.pyenv()
    require.pyenv.python(env.config["python"])
    require.pyenv.venv(env.env_name, env.config["python"])


def setup_db():
    """
    Require proper  PostgreSQL database server, user and database instance
    """
    require.postgres.server()
    require.postgres.user(env.db_settings["user"], env.db_settings["password"])
    require.postgres.database(
        env.db_settings["database"], env.db_settings["user"]
    )


def setup_server():
    """
    Require nginx server to be configured and serve project via uWSGI
    """
    require.nginx.server()
    require.uwsgi.uwsgi()

    uwsgi_plugin_name = env.config["project"]
    python_bin = os.path.join(
        pyenv.get_venv_path(env.env_name), "bin", "python"
    )
    require.uwsgi.python_plugin(python_bin, uwsgi_plugin_name)
    require.uwsgi.site(
        env.env_name, context={
            "project_dir": os.path.join(env.project_dir, env.config["project"]),
            "venv_dir": pyenv.get_venv_path(env.env_name),
            "env_name": env.env_name,
            "plugin_name": uwsgi_plugin_name,
            "plugins_dir": uwsgi.UWSGI_PLUGINS_LOCATION
        }, template_source="config/uwsgi/uwsgi-template.ini",
    )

    # todo: don't hardcode media and static paths
    require.nginx.site(
        env.env_name, template_source="config/uwsgi/nginx-template.conf",
        env_name=env.env_name,
        port=env.config["deployment"][env.stage_name]["nginx_port"],
        media_url="/media", media_root=os.path.join(env.project_dir, "media"),
        static_url="/static", static_root=os.path.join(env.project_dir, "static")
    )


def setup():
    """
    Simply run everythying (except setting up user) that is defined
    above using one command.
    """
    setup_project()
    setup_python()
    setup_db()
    setup_server()
