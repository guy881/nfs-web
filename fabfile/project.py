import json

from fabric.api import env

# load variable data from files
with open("fabconfig.json") as f:
    config = json.load(f)

# store them in env
env.config = config