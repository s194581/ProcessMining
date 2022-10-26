# coding=utf-8
""" Test if activity is blocked when milestone points to it"""
import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph


class EvaluateFRQ8Test1(unittest.TestCase):
    """
    Check if Include of a Nesting activity works properly
    """

    def setUp(self):
        """
        Set up unit test environment
        :return:
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation1.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_include_nesting_activity(self):
        """
        a - c - d does not work when c is not included by the occurrence of b
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.violated_traces['a  -c  -d'] == 2)
        self.assertTrue(self.ca.ViolatedActivities['c'] == 2)


class EvaluateFRQ8Test2(unittest.TestCase):
    """
    Check if exclude nesting activity is performed properly
    """

    def setUp(self):
        """
        Set up unit test environment
        :return:
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation2.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_exclude_nesting_activity(self):
        """
        b c e must fail 8 times
        a c d must not fail
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(len(self.ca.ViolatingTraces) == 8)
        self.assertTrue(self.violated_traces['b  -c  -e'] == 8)
        self.assertTrue(self.ca.ViolatedActivities['c'] == 8)
        self.assertTrue(self.ca.ViolatedActivities['e'] == 8)


class EvaluateFRQ8Test3(unittest.TestCase):
    """
    Check if pending response transition is correctly performed with Nesting activities
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation3.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_pending_response_target_nesting_activity(self):
        """
        b c e
        a c d
        case should work
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 0)


class EvaluateFRQ8Test4(unittest.TestCase):
    """
    Check if pending response transition works properly
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation4.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_pending_response_target_nesting_activity(self):
        """
        b c e traces should not work because d is Pending and thereby the Nesting activity is also pending
        a c d traces should work
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)

        self.assertTrue(self.violated_traces['b  -c  -e'] == 8)
        self.assertTrue(len(self.ca.ViolatingTraces))
        self.assertTrue(self.ca.ViolatedPending['d'] == 8)
        self.assertTrue(self.ca.ViolatedPending['NestingActivity'] == 8)


class EvaluateFRQ8Test5(unittest.TestCase):
    """
    Test nesting activity as pending response target
    """

    def setUp(self):
        """
        Set up unit test environment
        :return:
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation5.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_pending_response_target_nesting_activity(self):
        """
        b c e
        a c d makes e fail twice because it keeps pending
        case should work
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.ca.ViolatedPending['e'] == 2)


class EvaluateFRQ8Test6(unittest.TestCase):
    """

    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation6.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_exclude_target_nesting_activity(self):
        """
        b c e failes 8 times because 'e' is excluded by the exclusion of the nesting activity
        a c d
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.ca.ViolatedActivities['e'] == 8)
        self.assertTrue(self.violated_traces['b  -c  -e'] == 8)


class EvaluateFRQ8Test7(unittest.TestCase):
    """
    Test nesting activity as condition target
    """

    def setUp(self):
        """
        Set up unit test environment
        :return:
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation7.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_condition_target_nesting_activity(self):
        """
        condition from a to the nesting activity is introduced
        b c e fails 8 times because 'e' is blocked by the eclusion of the nesting activity
        a c d
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.violated_traces['b  -c  -e'] == 8)
        self.assertTrue(len(self.ca.ViolatedConnections) == 1)


class EvaluateFRQ8Test8(unittest.TestCase):
    """
    Tests a Nesting activity as an condition target
    """

    def setUp(self):
        """
        Set up unit test environment
        :return:
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation8.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_condition_target_nesting_activity(self):
        """
        b c e must not fail
        a c d must fail twice
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.violated_traces['a  -c  -d'] == 2)
        self.assertTrue(len(self.ca.ViolatedConnections) == 1)


class EvaluateFRQ8Test9(unittest.TestCase):
    """
    Checks if multiple milestones with nesting activities as sources are evaluated correctly
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation9.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_milestone_source_nesting_activity(self):
        """
        b c e must not fail
        a c d must fail twice
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.violated_traces['a  -c  -d'] == 2)
        self.assertTrue(len(self.ca.ViolatedConnections) == 1)


class EvaluateFRQ8Test10(unittest.TestCase):
    """
    Checks if multiple milestone connections toward a nesting activity can be evaluated
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation10.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_milestone_target_nesting_activity(self):
        """
        b c e never fails
        a c d must fail twice
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 1)
        self.assertTrue(self.violated_traces['a  -c  -d'] == 2)
        self.assertTrue(len(self.ca.ViolatedConnections) == 1)


class EvaluateFRQ8Test11(unittest.TestCase):
    """
    Special case with target of a nested activity
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation11.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_response_to_nested_activity(self):
        """
        b c e
        a c d
        all traces must end happily
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 0)


class EvaluateFRQ8Test12(unittest.TestCase):
    """
    Special case with three connections
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ8 input files/FRQ8evaluationlog1.xes'
        dcr_graph_path = 'FRQ8 input files/FRQ8_evaluation12.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)
        self.violated_traces = self.ca.create_violated_traces_dict()

    def test_three_connections(self):
        """
        b c e
        a c d
        No case should fail
        :return:
        """
        self.assertTrue(len(self.violated_traces) == 0)
