# coding=utf-8
""" Test FRQ3: Activity may not be included and pending at the process end"""
import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph


class EvaluateFRQ3Test1(unittest.TestCase):
    """
    First test case, activity a is initially pending for execution
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ3 input files/FRQ3evaluationlog1.xes'
        dcr_graph_path = 'FRQ3 input files/FRQ3_evaluation.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_FRQ3_a_is_included_and_pending_initially(self):
        """
        'a' occurs 2 times in the ten traces. Thus, 'a' must be Pending and Included 8 times
        """
        self.assertTrue(self.ca.ViolatedPending['a'] == 8)


class EvaluateFRQ3Test2(unittest.TestCase):
    """
    Test if the tool reacts positive when an activity is excluded
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ3 input files/FRQ3evaluationlog1.xes'
        dcr_graph_path = 'FRQ3 input files/FRQ3_evaluation2.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_FRQ3_activity_a_is_excluded(self):
        """
        'a' occurs 2 times in the ten traces. Thus, 'a' must violate the Included constraint twice and no
        pending constraint may not be found.
        :return:
        """
        self.assertTrue(self.ca.ViolatedActivities['a'] == 2)
        self.assertTrue(self.ca.ViolatedPending == {})
