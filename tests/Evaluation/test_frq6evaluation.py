# coding=utf-8
""" Test if activity is blocked when milestone points to it"""
import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph


class EvaluateFRQ6Test1(unittest.TestCase):
    """
    Check if an activity can be blocked by a milestone
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ6 input files/FRQ6evaluationlog1.xes'
        dcr_graph_path = 'FRQ6 input files/FRQ6_evaluation.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_milestone_between_b_and_c(self):
        """
        'b' is initially pending and occurs 8 times before 'c' in the ten traces. Thus, 'c' is prohibited 2 times
        """
        self.assertTrue(len(self.ca.ViolatedConnections) == 1)
        self.assertTrue(self.ca.ViolatedConnections['milestone-b-c'] == 2)
        self.assertTrue(self.ca.ViolatedPending['b'] == 2)


class EvaluateFRQ6Test2(unittest.TestCase):
    """
    Evaluate different process trace
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ6 input files/FRQ6evaluationlog1.xes'
        dcr_graph_path = 'FRQ6 input files/FRQ6_evaluation2.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_milestone_between_a_and_c(self):
        """
        'a' is in Pending and occurs 2 times before 'c' in the ten traces. Thus, 'c' is prohibited 8 times
        """
        self.assertTrue(len(self.ca.ViolatedConnections) == 1)
        self.assertTrue(self.ca.ViolatedConnections['milestone-a-c'] == 8)
        self.assertTrue(self.ca.ViolatedPending['a'] == 8)


class EvaluateFRQ5Test3(unittest.TestCase):
    """
    Test if the milestone is not included when the source activity is not included too
    """

    def setUp(self):
        event_log_path = 'FRQ6 input files/FRQ6evaluationlog1.xes'
        dcr_graph_path = 'FRQ6 input files/FRQ6_evaluation3.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_milestone_between_a_and_c_a_not_included(self):
        """
        'a' is in Pending and occurs 2 times before 'c' in the ten traces. Thus, 'a' violates the activity executed while
        not included constraint and the violated connections must be empty.
        :return:
        """
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['a'] == 2)
        self.assertFalse(bool(self.ca.ViolatedConnections))
