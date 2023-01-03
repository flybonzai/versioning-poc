import yaml


def load_yaml_config(file_path):
    with open(file_path, 'r') as inf:
        return yaml.safe_load(inf)


def load_changelog():
    return load_yaml_config('conf/version_changelog.yml')


def load_event_types():
    return load_yaml_config('conf/event-types.yml')


def load_fields(destination_name):
    return load_yaml_config(f'conf/{destination_name}-fields.yml')
