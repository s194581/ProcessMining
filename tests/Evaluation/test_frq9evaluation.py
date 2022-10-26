# coding=utf-8
"""
Used to check if guards referencing to data of another event can be checked
"""
import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph


class EvaluateFRQ9Test1(unittest.TestCase):
    """
    a is augmented with data, and checked if it can
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ9 input files/FRQ9evaluationlog1.xes'
        dcr_graph_path = 'FRQ9 input files/FRQ9_evaluation1.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_expression_related_to_different_event_transition(self):
        """
        For the transition and Include connection is used
        a - c - d does not work when d is not included because of the data constraint related to a
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.violated_traces['a  -c  -d'] == 1)
        self.assertTrue(self.ca.ViolatedActivities["d"] == 1)


class EvaluateFRQ9Test2(unittest.TestCase):
    def setUp(self):
        """
        Set up unit test environment
        :return:
        """
        event_log_path = 'FRQ9 input files/FRQ9evaluationlog2.xes'
        dcr_graph_path = 'FRQ9 input files/FRQ9_evaluation2.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_expression_related_to_different_event_milestone(self):
        """
        The milestone between e and d is only active at one occurrence of a and thereby must fail once
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.violated_traces['a  -c  -d  -e'] == 1)
        self.assertTrue(self.ca.ViolatedConnections['milestone-e-d'] == 1)
