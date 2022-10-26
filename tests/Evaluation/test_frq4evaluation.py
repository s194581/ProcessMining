import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph

""" Test if the activity"""


class EvaluateFRQ1Test1(unittest.TestCase):
    def setUp(self):
        event_log_path = 'FRQ4 input files/FRQ4evaluationlog1.xes'
        dcr_graph_path = 'FRQ4 input files/FRQ4_evaluation.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_FRQ1_all_roles_match_correctly(self):
        # Test if Response marking change worked
        self.assertTrue(len(self.ca.ViolatedPending) == 1)
        self.assertTrue(self.ca.ViolatedPending['a'] == 2)

        # Check if include and exclude markings worked
        self.assertTrue(len(self.ca.ViolatedActivities) == 2)
        self.assertTrue(self.ca.ViolatedActivities['c'] == 2)
        self.assertTrue(self.ca.ViolatedActivities['e'] == 8)
