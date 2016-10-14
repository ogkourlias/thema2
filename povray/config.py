import configparser

class Config(object):
    ''' Exposes all settings listed in a valid configuration file (*.ini) as
        object attributes. Use as Config.setting, i.e. Config.Quality '''

    def __init__(self, config_file):
        ''' Read a configuration file '''
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def __getattr__(self, key):
        ''' Retrieves a setting regardless the section that contains it and
            offers it as an object attribute '''
        value = [self.config[section].get(key) 
                 for section in self.config.sections() 
                 if self.config[section].get(key)]
        try:
            value = float(value[0])
        except ValueError:
            return value[0]
        except IndexError:
            return value
        return value
