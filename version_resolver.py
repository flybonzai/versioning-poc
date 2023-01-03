from pprint import pprint
from yaml_utils import *
from collections import defaultdict
from itertools import dropwhile

RESOLVED_SCHEMA = 'resolved_schema'
REMOVED_EVENTS = 'removed_events'
REMOVED_FIELDS_BY_EVENT = 'removed_fields_by_event'


def resolve_versions(changelog, schema_version, events):
    resolved_version = make_latest_version(events)
    for destination, events in resolved_version.items():
        resolved_version[destination] = {
            RESOLVED_SCHEMA: events,
            REMOVED_EVENTS: [],
            REMOVED_FIELDS_BY_EVENT: defaultdict(list)
        }
    changelog_versions = changelog['versions']
    newer_versions = list(dropwhile(lambda x: schema_version not in x, changelog_versions))[1:]
    for newer_version in newer_versions:
        for version, version_data in newer_version.items():
            event_types = version_data['event_types']
            fields_for_events = version_data['fields']
            for destination, destination_events in event_types.items():
                for destination_event in destination_events:
                    resolved_version[destination][REMOVED_EVENTS].append(destination_event)
                    resolved_version[destination][RESOLVED_SCHEMA].pop(destination_event)

            for destination, events_to_fields in fields_for_events.items():
                for event, event_fields in events_to_fields.items():
                    maybe_latest_version_of_event = resolved_version[destination][RESOLVED_SCHEMA].get(event)
                    if maybe_latest_version_of_event:
                        for event_field in event_fields:
                            resolved_version[destination][REMOVED_FIELDS_BY_EVENT][event].append(event_field)
                            maybe_latest_version_of_event.remove(event_field)
                    else:
                        continue
    return resolved_version


def make_latest_version(events_data):
    http_destinations = events_data['currents']['http_destinations']
    latest_version = defaultdict(dict)

    for destination, attrs in http_destinations.items():
        fields_data = load_fields(destination.lower())
        fields = fields_data['fields']
        shared_fields = fields['shared']
        event_fields = {k: v for k, v in fields.items() if k != 'shared'}
        supported_events = attrs['supported_events']
        for supported_event in supported_events:
            latest_version[destination][supported_event] = sorted(event_fields[supported_event] + shared_fields)
    return latest_version


if __name__ == '__main__':
    events = load_event_types()
    changelog = load_changelog()
    resolved = resolve_versions(changelog, 'v_2', events)
    pprint(dict(resolved))
