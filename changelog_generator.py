from yaml_utils import *


def generate_new_changelog_for_destination(previous_version_data, current_version_data, destination_name):
    previous_fields = previous_version_data['fields']
    current_fields = current_version_data['fields']
    event_types_dict = {destination_name: []}
    fields_dict = {destination_name: {}}
    changelog = {'event_types': event_types_dict, 'fields': fields_dict}

    newly_added_events = set(current_fields) - set(previous_fields)

    event_types_dict[destination_name] = sorted(list(newly_added_events))

    for event_name, current_event_fields in current_fields.items():
        previous_event_fields = previous_fields.get(event_name)
        if previous_event_fields is None:
            fields_dict[destination_name][event_name] = sorted(current_event_fields + current_fields['shared'])
        else:
            fields_diff_for_event = set(current_event_fields) - set(previous_event_fields)
            if fields_diff_for_event:
                fields_dict[destination_name][event_name] = sorted(list(fields_diff_for_event))

    return changelog


def merge_changelogs(changelog1, changelog2, schema_version):
    return {
        schema_version: {
            'event_types': {**changelog1['event_types'], **changelog2['event_types']},
            'fields': {**changelog1['fields'], **changelog2['fields']}
        }
    }


def append_new_changelog_entry(changelog, new_changelog_entry):
    changelog['versions'].append(new_changelog_entry)


if __name__ == '__main__':
    amplitude_changelog = generate_new_changelog_for_destination(load_fields('amplitude_v2'), load_fields('amplitude'),
                                                                 'AMPLITUDE')
    segment_changelog = generate_new_changelog_for_destination(load_fields('segment_v2'), load_fields('segment'),
                                                               'SEGMENT')
    merged = merge_changelogs(amplitude_changelog, segment_changelog, 'v_3')
    print(yaml.dump(merged, default_flow_style=False))

    old_changelog = load_yaml_config('conf/version_changelog_v2.yml')
    append_new_changelog_entry(old_changelog, merged)
    print(yaml.dump(old_changelog, default_flow_style=False))
