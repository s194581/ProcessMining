from __future__ import division
import json
import xml.etree.ElementTree as ET
import sys
import Engine
import copy


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
                for x in trace:

                    if x.attrib.get('key') == 'concept:name':
                        key = x.attrib.get('value')
                        events.append(key)
                        dict.append(events)
    return dict

# Assumption - *When* the trace fails has an impact on *how* conforming it is


def find_pending(p, e):
    for e in p.pending:
        if e in p.included:
            for r in p.relations:
                if r.src != e:
                    continue
                elif r.rel == "include":
                    return r.src
    return None


def our_conf(traces, p):
    nr_traces = len(traces)
    # Do some conformance checking
    percent_executed = 0
    extra_events = 0
    missing_events = 0
    violation_percent = 0
    for trace in traces:
        copy_p = copy.deepcopy(p)
        # Check the trace
        violation = 0
        missing = 0
        for event in trace:

            if event in copy_p.enabled():
                copy_p.execute(event)
                # modify so we can continue
            else:
                missing += 1
                pass
        if not copy_p.is_accepting():
            for e in copy_p.pending:
                if e in copy_p.enabled():
                    violation += 1
        violation_percent += max((violation /
                                 len(copy_p.events), (missing/len(trace))))

    # print(missing_events)
    conf_val = 1-(violation_percent)/len(traces)
    return conf_val


def progress_based_conf(traces, p):

    nr_traces = len(traces)
    # Do some conformance checking
    percent_executed = 0
    for trace in traces:
        copy_p = copy.deepcopy(p)
        # Check the trace
        nr_executed = 0
        for event in trace:

            if event in copy_p.enabled():
                copy_p.execute(event)
                # modify so we can continue
                nr_executed += 1
            else:
                break
        percent_executed += nr_executed/len(trace)

    conf_val = (percent_executed/nr_traces)
    return conf_val

# Simple value. Assumption - Trace fails = no conformance


def simple_conf(traces, p):
    fails = 0
    nr_traces = len(traces)
    # Do some conformance checking
    for trace in traces:
        flag = False
        # Check the trace
        copy_p = copy.deepcopy(p)
        for event in trace:
            if event in copy_p.enabled():
                copy_p.execute(event)
            else:
                flag = True
                break
        if flag:
            fails += 1
        elif not copy_p.is_accepting():
            fails += 1

    #print(fails, nr_traces)
    conf_val = 1.0-(fails/nr_traces)
    return conf_val


def main():
    #args = sys.argv[1:]
    # Create DCR graph
    p = DCR_graph(
        "ConformanceChecking/Data/Train/Train_XES/Sendmail_train.txt.JSON")
    # p = DCR_graph(args[0]) # As argument on commandline

    # Create traces from xes file
    # traces = read_log_from_XES(args[1]) # As argument on commandline
    traces = read_log_from_XES(
        'ConformanceChecking/Data/Test/Test_XES/Approvals_test.xes')

    simple_conf_val = simple_conf(traces, p)
    print("Simple conformance value: ", simple_conf_val)

    progress_based_conf_val = progress_based_conf(traces, p)
    print("Progress based conformance value: ", progress_based_conf_val)

    our_conf_val = our_conf(traces, p)
    print("our conformance value: ", our_conf_val)


if __name__ == "__main__":
    main()
