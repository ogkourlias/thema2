from povray import config

## Default configuration file located in the project root
DEFAULT_CONFIG = 'default.ini'
## Create a SETTINGS object containing all the settings as attributes.
## Use as SETTINGS.Quality, SETTINGS.MovieFPS, etc.
SETTINGS = config.Config(DEFAULT_CONFIG)

def load_config(config_file):
    return config.Config(config_file)