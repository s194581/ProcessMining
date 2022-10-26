# coding=utf-8
"""Import an event log from a Celonis server instance"""
from xml.etree import ElementTree as ETree

import pandas as pd

from eventlog import EventLog, Event, Trace


def create_index_mapping(index_file):
    """
    A config file is required since in Celonis tables are named differently because naming
    rules in Python infere with Celonis Table namings
    :param index_file:
    :return: the mapping between the data and index
    """
    config_xml = ETree.parse(index_file)
    root = config_xml.getroot()
    index_mapping = {}
    for index in root.iter('index'):
        index_mapping[index.get('data')] = int(index.get('id'))
    return index_mapping


def get_event_log_from_celonis():
    """
    Used to retrieve the event log data structure from a celonis instance
    :return:
    """

    index_file = '1000 input/celonis.xml'
    index_mapping = create_index_mapping(index_file)

    username = "ho87nyze"
    port = 443
    hostname = "celonis.is.rw.fau.de"
    token = "3f2c0684-e639-41b5-96ba-79c70f97c332"  # obtained from the MyProfile page
    secret = "dR0pNb3WyoWlel6lSGG8SU3qGwnJmrMgMqXeYtfvMWSvddaMFhBsRZvjW4Y1KJhf"  # obtained from the MyProfile page
    api_prefix = ""  # can be found in the urs you use to login:
    #   examples:
    #   https://10.0.0.1:9000/cpm/welcome => "cpm"
    #   https://10.0.0.1/services/celonis/welcome => "services/celonis"
    #   https://10.0.0.1:9000/welcome => ""

    use_tls = True  # True if you use a HTTPS connection to your celonis instance, else False

    cel = Celonis(username=username, hostname=hostname, use_tls=use_tls,
                  api_prefix=api_prefix, api_secret=secret, api_token=token, port=port)

    analysis_id = 185
    analysis = cel.analysis(analysis_id)
    dm = analysis.data_model()
    activity_tables = dm.get_activity_tables()
    activity_table: pd.DataFrame = dm.get_table(activity_tables[0])

    event_log = EventLog()

    case_col = activity_table.columns[index_mapping['case_id'] - 1]
    time_stamp_col = activity_table.columns[index_mapping['timestamp'] - 1]
    if 'lifecycle:state' in index_mapping:
        life_cycle_col = activity_table.columns[index_mapping['lifecycle:state'] - 1]
        activity_table = activity_table[activity_table[life_cycle_col] == "COMPLETE"]
    clean_activity_table = activity_table.sort_values([time_stamp_col, case_col])

    for row in clean_activity_table.itertuples():
        case_id = int(row[index_mapping['case_id'] + 1]) - 1
        if len(event_log.Traces) <= case_id:
            event_log.append_trace(Trace(case_id))
        lower_lc = row[index_mapping["lifecycle:state"] + 1].lower()
        if lower_lc != 'complete':
            continue
        event_name = row[index_mapping["event_name"] + 1]
        event_role = row[index_mapping["event_role"] + 1]
        time_stamp = row[index_mapping["timestamp"] + 1]
        event_log.Traces[case_id].append_event(Event(event_name, event_role, time_stamp))

    return event_log
