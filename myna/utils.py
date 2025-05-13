import os
import configparser
import subprocess

# Paths
BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "myna.cfg")
ALIASES_PATH = os.path.join(BASE_DIR, "aliases.cfg")

# Load general config (myna.cfg)
def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config

# Load aliases from aliases.cfg
def load_aliases():
    config = configparser.ConfigParser()
    config.read(ALIASES_PATH)
    return dict(config["aliases"]) if "aliases" in config else {}

# Save aliases to aliases.cfg
def save_aliases(aliases):
    config = configparser.ConfigParser()
    config["aliases"] = aliases
    with open(ALIASES_PATH, "w") as configfile:
        config.write(configfile)

# Run shell command
def run_shell_command(cmd):
    subprocess.run(cmd, shell=True)
