# coding=utf-8
"""
Checks the FRQ2 Test if activity is included when its related event occurs
"""
import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph


class EvaluateFRQ2Test1(unittest.TestCase):
    """
    No Violations of the included constraint
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ2 input files/FRQ2evaluationlog1.xes'
        dcr_graph_path = 'FRQ2 input files/FRQ2_evaluation.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_FRQ2_all_activities_included(self):
        """
        Conformance analysis data Violated activities must be empty
        """
        self.assertFalse(bool(self.ca.ViolatedActivities))


class EvaluateFRQ2Test2(unittest.TestCase):
    """
    Activity a is excluded from the DCR graphs
    """

    def setUp(self):
        """
        Set up the unit test environment
        :return:
        """
        event_log_path = 'FRQ2 input files/FRQ2evaluationlog1.xes'
        dcr_graph_path = 'FRQ2 input files/FRQ2_evaluation2.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_FRQ2_activity_a_is_excluded(self):
        """
        Activity a is executed twice during the event log in two different traces
        """
        self.assertTrue(self.ca.ViolatedActivities['a'] == 2)
        self.ca.ViolatedActivities.pop('a')
        self.assertTrue(self.ca.ViolatedActivities == {})
