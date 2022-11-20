from __future__ import division
import json
import xml.etree.ElementTree as ET
import sys
import Engine


def create_nodes(jsongraph, p):
    nodes = set()

    for edge in jsongraph:
        s = edge['source']
        t = edge['target']
        nodes.add(t)
        nodes.add(s)

    for x in nodes:
        p.add_event(x)


def create_edges(jsongraph, p):
    for edge in jsongraph:
        s = edge['source']
        t = edge['target']
        r = edge['type']
        p.add_relation(s, r, t)


def create_graph(jsongraph, p):
    create_nodes(jsongraph, p)
    create_edges(jsongraph, p)


def DCR_graph(jsonfile):
    f = open(jsonfile).read()
    file = json.loads(f)

    jsongraph = file['Relation']
    p = Engine.Process()
    create_graph(jsongraph, p)

    return p


def read_log_from_XES(filename):
    dict = []
    tree = ET.parse(filename)
    root = tree.getroot()

    for child in root:
        events = []

        for trace in child:
            case_id = trace.attrib.get('value')

            if case_id == None:
                key = trace[1].attrib.get('value')
                events.append(key)
                dict.append(events)
    return dict

# Assumption - *When* the trace fails has an impact on *how* conforming it is


def progress_based_conf(traces, p):
    nr_traces = len(traces)
    # Do some conformance checking
    percent_executed = 0
    for trace in traces:
        # Check the trace
        nr_executed = 0
        for event in trace:
            p.execute(event)
            # C# code
            if not p.is_accepting():
                break
            else:
                nr_executed += 1
        percent_executed += nr_executed/len(trace)

    conf_val = (percent_executed/nr_traces)
    return conf_val

# Simple value. Assumption - Trace fails = no conformance


def simple_conf(traces, p):
    fails = 0
    nr_traces = len(traces)
    # Do some conformance checking
    for trace in traces:
        # Check the trace
        for event in trace:
            # C# code
            p.execute(event)
            if not p.is_accepting():
                fails += 1
                break
    conf_val = 1.0-(fails/nr_traces)
    return conf_val


def main():
    args = sys.argv[1:]
    # Create DCR graph
    p = DCR_graph(
        "morten.txt.JSON")
    # p = DCR_graph(args[0]) # As argument on commandline

    # Create traces from xes file
    # traces = read_log_from_XES(args[1]) # As argument on commandline
    traces = read_log_from_XES(
        'morten.xes')

    simple_conf_val = simple_conf(traces, p)
    print("Simple conformance value: ", simple_conf_val)

    progress_based_conf_val = progress_based_conf(traces, p)
    print("Progress based conformance value: ", progress_based_conf_val)


if __name__ == "__main__":
    main()
