from povray import config
import logging
import sys

# Default configuration file located in the project root
DEFAULT_CONFIG = 'default.ini'
# Create a SETTINGS object containing all the settings as attributes.
# Use as SETTINGS.Quality, SETTINGS.MovieFPS, etc.
SETTINGS = config.Config(DEFAULT_CONFIG)

# Setup logging, reading log-level from the configuration file
logging.basicConfig(level=logging._nameToLevel[SETTINGS.LogLevel])
logger = logging.getLogger(__name__)

logger.info('["%s"] - Using config file "%s"', sys._getframe().f_code.co_name, DEFAULT_CONFIG)


def load_config(config_file):
    logger.info('["%s"] - Loading config file "%s"', sys._getframe().f_code.co_name, config_file)
    return config.Config(config_file)