import os

from fabric.api import cd, env


class Environment():
    def __init__(self, name, env_data=None):
        if not env_data:
            env_data = {}

        env_name = "{0}-{1}".format(
            env.config["project"], name
        )
        env_data.update({
            "stage_name": name,
            "env_name": env_name,
            "hosts": env.config["deployment"][name]["hosts"],
            "python_requirements": env.config["deployment"][name].get(
                "python-requirements", "requirements.txt"
            ),
            "db_settings": {
                "user": env.config["project"],
                "database": env_name,
                "password": env.get("DB_PASSWORD", env.config["project"])
            }
        })
        parent_dir = env_data.get("parent_dir")
        if parent_dir:
            env_data["project_dir"] = os.path.join(parent_dir, env_name)

        self.data = env_data
        self.name = env_name

    def __call__(self):
        for k, v in self.data.items():
            env[k] = v
        if "project_dir" in env:
            cd(env.project_dir)


develop = Environment("aruba", {
    "username": env.config["project"],
    "parent_dir": os.path.join("/", "var", "www"),
    "DB_PASSWORD": 'asdasd12'
})

pi3 = Environment("pi3", {
    "username": env.config["project"],
    "parent_dir": os.path.join("/", "var", "www"),
    "DB_PASSWORD": 'asdasd12'
})
