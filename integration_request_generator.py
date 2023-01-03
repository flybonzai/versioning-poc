from version_resolver import *

TEST_INTEGRATION = {
    'app_group_id': 'test_id_amplitude',
    'platform_cluster': 'dev',
    'destination_name': 'Amplitude',
    'status': 'enabled',
    'name': 'test_name',
    'partitions': 3,
    'event_type_configs': [
        'event1',
        'event2',
        'event3',
        'event5'
    ],
    'destination_config': {
        'encrypted_api_key': 'test_api_key',
        'encrypted_api_key_initial_vector': 'test_api_key_iv',
        'num_connections': 3,
        'region': 'US'
    },
    'event_field_transformations': {
        'field_a': 'sha256'
    },
    'event_field_mappings': {},
    'scaling_config': {'max_connect_tasks': 3, 'min_connect_tasks': 1}
}


def generate_request(current_integration_data, target_schema_version):
    resolved = resolve_versions(load_changelog(), target_schema_version, load_event_types())
    destination_name = current_integration_data['destination_name'].upper()
    resolved_for_destination = resolved[destination_name]
    event_type_configs = current_integration_data['event_type_configs']
    event_field_transformations = current_integration_data['event_field_transformations']

    for event in event_type_configs:
        if event in resolved_for_destination[REMOVED_EVENTS]:
            event_type_configs.remove(event)

    for event_name, event_fields in resolved_for_destination[REMOVED_FIELDS_BY_EVENT].items():
        for event_field in event_fields:
            event_field_transformations[event_field] = 'drop'

    return current_integration_data


if __name__ == '__main__':
    integration_data = generate_request(TEST_INTEGRATION, 'v_1')
    pprint(integration_data)
