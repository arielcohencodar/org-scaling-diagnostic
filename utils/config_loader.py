import toml

def load_config():
    with open('config.toml', 'r') as config_file:
        return toml.load(config_file)

config = load_config()
