# coding=utf-8
"""
 Test if connection is deactivated because of a guard. For this evaluation the Include connection is taken as a
 representative
"""
import unittest

import cc_dcr
import eventlog_parser
from conf_data import ConformanceAnalysisData
from graph import DCRGraph


class EvaluateFRQ7Test1(unittest.TestCase):
    """
    Check if expression with included is checked correctly
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ7 input files/FRQ7evaluationlog1.xes'
        dcr_graph_path = 'FRQ7 input files/FRQ7_evaluation.xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def tearDown(self):
        """
        Unit test tear down
        """
        del self.dcr_graph
        del self.event_log
        del self.ca

    def test_include_with_guard_equal_between_b_and_c(self):
        """
        'b' occurs 8 times before 'c' in the ten traces 4 times with valid expression.
        Thus, 'c' is prohibited 4 times because 'a' occurs two times
        :return:
        """
        self.assertTrue(len(self.ca.ViolatingTraces) == 6)
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['c'] == 6)


class EvaluateFRQ7Test2(unittest.TestCase):
    """
    Check if != can be evaluated within a guard
    """

    def setUp(self):
        """
        Unit test setup
        :return:
        """
        event_log_path = 'FRQ7 input files/FRQ7evaluationlog1.xes'
        dcr_graph_path = 'FRQ7 input files/FRQ7_evaluation (1).xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_include_with_guard_not_equal_between_b_and_c(self):
        """
        'b' occurs 8 times before 'c' in the ten traces, thereby the data is not equal twice.
        Thus, 'c' is only added to Include twice and subsequently violated 6 times
        """
        self.assertTrue(len(self.ca.ViolatingTraces) == 6)
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['c'] == 6)
        self.ca.ViolatedActivities.pop('c')
        self.assertTrue(self.ca.ViolatedActivities == {})

    def tearDown(self):
        """
        Unit test tear down
        :return:
        """
        del self.dcr_graph
        del self.event_log
        del self.ca


class EvaluateFRQ7Test3(unittest.TestCase):
    """
    Check greater than with no value greater than the reference
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ7 input files/FRQ7evaluationlog1.xes'
        dcr_graph_path = 'FRQ7 input files/FRQ7_evaluation (2).xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_include_with_guard_gt_comparator(self):
        """
        Data is never greater than the reference. Thus c is never included and fails at every occurrence.
        :return:
        """
        self.assertTrue(len(self.ca.ViolatingTraces) == 10)
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['c'] == 10)
        self.ca.ViolatedActivities.pop('c')
        self.assertTrue(self.ca.ViolatedActivities == {})

    def tearDown(self):
        """
        Unit test tear down
        :return:
        """
        del self.dcr_graph
        del self.event_log
        del self.ca


class EvaluateFRQ7Test4(unittest.TestCase):
    def setUp(self):
        """
        Unit test set up environment
        """
        event_log_path = 'FRQ7 input files/FRQ7evaluationlog2.xes'
        dcr_graph_path = 'FRQ7 input files/FRQ7_evaluation (2).xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_include_with_guard_gt_comparator(self):
        """
        Same test as Test3 but with different event log this time two values are higher than the reference.
        Thus 'c' is included twice and fails 8 times
        """
        self.assertTrue(len(self.ca.ViolatingTraces) == 8)
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['c'] == 8)
        self.ca.ViolatedActivities.pop('c')
        self.assertTrue(self.ca.ViolatedActivities == {})

    def tearDown(self):
        """
        Unit test tear down
        """
        del self.dcr_graph
        del self.event_log
        del self.ca


class EvaluateFRQ7Test5(unittest.TestCase):
    """
    Greater than equal with include
    """

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ7 input files/FRQ7evaluationlog2.xes'
        dcr_graph_path = 'FRQ7 input files/FRQ7_evaluation (3).xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_include_with_guard_gte_comparator(self):
        """
        'b' occurs 8 times before c and thereby has three values that are greater or equal than the reference.
        Thus 'c' is not included at execution five times
        """
        self.assertTrue(len(self.ca.ViolatingTraces) == 5)
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['c'] == 5)
        self.ca.ViolatedActivities.pop('c')
        self.assertTrue(self.ca.ViolatedActivities == {})

    def tearDown(self):
        """
        Unit test tear down
        :return:
        """
        del self.dcr_graph
        del self.event_log
        del self.ca


class EvaluateFRQ7Test6(unittest.TestCase):
    """Checks int as reference type with lt"""

    def setUp(self):
        """
        Set up unit test environment
        """
        event_log_path = 'FRQ7 input files/FRQ7evaluationlog2.xes'
        dcr_graph_path = 'FRQ7 input files/FRQ7_evaluation (4).xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_include_with_guard_lt_comparator(self):
        """
        the value in b is lower than the reference once. Thus c is included once and thereby the overall failure of
        traces is 9
        :return:
        """
        self.assertTrue(len(self.ca.ViolatingTraces) == 9)
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['c'] == 9)
        self.ca.ViolatedActivities.pop('c')
        self.assertTrue(self.ca.ViolatedActivities == {})


class EvaluateFRQ7Test7(unittest.TestCase):
    """Checks float as reference type with lte"""

    def setUp(self):
        """
        Set up unit test environment
        :return:
        """
        event_log_path = 'FRQ7 input files/FRQ7evaluationlog3.xes'
        dcr_graph_path = 'FRQ7 input files/FRQ7_evaluation (5).xml'
        self.dcr_graph = DCRGraph.get_graph_instance(dcr_graph_path)
        self.event_log = eventlog_parser.get_event_log(event_log_path)
        self.ca = ConformanceAnalysisData()
        cc_dcr.add_dcr_graph_for_test(self.dcr_graph)
        for trace in self.event_log.Traces:
            cc_dcr.perform_conformance_checking(trace, self.ca)

    def test_include_with_guard_lte_comparator(self):
        """
        In this event log all in all 4 values are lower than or equal to the reference value. Thus C is included 4 times
        and thereby 6 traces do still fail
        :return:
        """
        self.assertTrue(len(self.ca.ViolatingTraces) == 6)
        self.assertTrue(bool(self.ca.ViolatedActivities))
        self.assertTrue(self.ca.ViolatedActivities['c'] == 6)
        self.ca.ViolatedActivities.pop('c')
        self.assertTrue(self.ca.ViolatedActivities == {})
