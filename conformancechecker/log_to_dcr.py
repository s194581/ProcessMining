from graph import DCRGraph
import csv
import pandas as pd

def findActivities():
    log = pd.read_csv("Resources/Approvals.csv",sep=',', encoding='latin1')
    events= log[['label_EventName']]
    
    s = set()
    for index,event in log.iterrows():
        s.add(event['label_EventName'])
    
    return s

G = findActivities();

def dcrMiner():
    # G is the graph
    
    # G = all activities
    G = findActivities();
    print(G)

    # For all x in G, set x excluded, pending, not executed in G

    # For all possible pairs (x,y) where x and y are in G, set condition *<-, response *->, exclusion %->

    # For all *trace* in traces:
    # set the initial event t0 to included
    # remove all conditions leading to t0 in G

    # For all t in traces
    # Set initial p = t0(start node)

    # For all events in the trace: (i =1;i<t.length)
        # remove p->%t_i from G
        # add p ->+ t_i to G
        # For all x where t_i *<- x in G:
            # If x does not occur t_i in the trace:
                # Remove t_i *<- x from G
                
        # For all x where t_i *-> x:
            # If x does not occur after t_i in the trace:
                # Remove t_i *-> x from G
        # p = t_i
    # For all activities not in the trace:
        # Set a not pending in G
    
    # Return G

dcrMiner()