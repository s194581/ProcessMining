# coding=utf-8
"""
Evaluation of FRQ5: Test if activity is blocked when condition points to it
"""
import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph


class EvaluateFRQ5Test1(unittest.TestCase):
    """
    A condition from b to c is introduced to the dcr graph
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ5 input files/FRQ5evaluationlog1.xes'
        dcr_graph_path = 'FRQ5 input files/FRQ5_evaluation.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_condition_between_b_and_c(self):
        """
        'b' occurs 8 times before 'c' in the ten traces. Thus, 'c' is prohibited 2 times
        :return:
        """
        self.assertTrue(len(self.ca.ViolatedConnections) == 1)
        self.assertTrue(self.ca.ViolatedConnections['condition-b-c'] == 2)


class EvaluateFRQ5Test2(unittest.TestCase):
    """
    In this case a condition is introduced between a and c instead
    """

    def setUp(self):
        """
        Unit test setup
        :return:
        """
        event_log_path = 'FRQ5 input files/FRQ5evaluationlog1.xes'
        dcr_graph_path = 'FRQ5 input files/FRQ5_evaluation2.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_condition_between_a_and_c(self):
        """
        'a' occurs 2 times before 'c' in the ten traces. Thus, 'c' is prohibited 8 times
        :return:
        """
        self.assertTrue(len(self.ca.ViolatedConnections) == 1)
        self.assertTrue(self.ca.ViolatedConnections['condition-a-c'] == 8)


class EvaluateFRQ5Test3(unittest.TestCase):
    """
    Check if the condition is inactive when the source node is excluded from the graph
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ5 input files/FRQ5evaluationlog1.xes'
        dcr_graph_path = 'FRQ5 input files/FRQ5_evaluation3.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_condition_between_a_and_c_a_not_included(self):
        """
        'a' is not included and occurs two times before 'c'. However since a is not included it may never be blocked
        """
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['a'] == 2)
        self.assertFalse(bool(self.ca.ViolatedConnections))
