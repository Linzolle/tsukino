import configparser

class Config:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.token = config.get('Credentials', 'Token', fallback=None)

        self.prefix = config.get('Misc', 'Prefix', fallback='$')
        
        if not self.token:
            raise ValueError('A token was not specified.')