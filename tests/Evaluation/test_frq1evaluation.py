# coding=utf-8
"""
Tests the fulfilment of the FRQ1
"""
import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph

""" Test if activity role matches the event role or not"""


class EvaluateFRQ1Test1(unittest.TestCase):
    """
    First Test Case that checks if no event infringed any role constraint
    """

    def setUp(self):
        """
        Sets up the unit test environment
        """
        event_log_path = 'FRQ1 input files/FRQ1evaluationlog1.xes'
        dcr_graph_path = 'FRQ1 input files/FRQ1_evaluation.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_FRQ1_all_roles_match_correctly(self):
        """
        Tests if there is no violated role in the conformance analysis data after execution
        """
        self.assertFalse(bool(self.ca.ViolatedRoles))


class EvaluateFRQ1Test2(unittest.TestCase):
    """
    Three roles are substituted by wrong roles in the event log
    """

    def setUp(self):
        """
        Sets up the unit test environment
        """
        event_log_path = 'FRQ1 input files/FRQ1evaluationlog2.xes'
        dcr_graph_path = 'FRQ1 input files/FRQ1_evaluation.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_FRQ1_three_roles_do_not_match(self):
        """
        The violated roles dict must have three violations
        Role3 instead of Role2 must occur once
        Role2 instead of Role3 must occur once
        Role4 instead of Role5 must occur once
        :return:
        """
        self.assertTrue(bool(self.ca.ViolatedRoles))
        self.assertTrue(len(self.ca.ViolatedRoles) == 3)
        reference_violated_roles = {"Role3 instead of Role2": 1, "Role2 instead of Role3": 1,
                                    "Role4 instead of Role5": 1}
        self.assertTrue(reference_violated_roles == self.ca.ViolatedRoles)
