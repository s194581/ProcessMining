# coding=utf-8
"""
Used to test markings
"""
import os
import unittest
from unittest.mock import MagicMock

import graph
from conn import Exclude, Include, DCRConnection, ConnectionTypes
from marking import Marking


class TestMarkingFunctions(unittest.TestCase):

    def setUp(self):
        """
        set up unit test environment
        """
        file_path = os.path.join(os.path.dirname(__file__), 'test_resources/TestCase_Milestone_Condition.xml')
        self.DCRGraph = graph.DCRGraph(file_path)
        self.InitialMarking = Marking.get_initial_marking()

    def test_initial_marking(self):
        self.assertEqual(4, len(self.InitialMarking.Included))
        dcr_graph: graph.DCRGraph = graph.DCRGraph.get_graph_instance()
        for node in dcr_graph.Nodes:
            self.assertTrue(node in self.InitialMarking.Included)
        response_node = dcr_graph.get_node('Activity0')
        self.assertIn(response_node, self.InitialMarking.PendingResponse)

    def test_copy_of_marking(self):
        deepcopy_test = Marking.get_initial_marking()
        self.assertNotEqual(self.InitialMarking, deepcopy_test)

        deepcopy_test.Included.remove(self.DCRGraph.get_node('Activity0'))
        deepcopy_test.Included.remove(self.DCRGraph.get_node('Activity2'))
        deepcopy_test.Executed.append(self.DCRGraph.get_node('Activity0'))
        deepcopy_test.Executed.append(self.DCRGraph.get_node('Activity2'))

        # Check different lens
        self.assertEqual(4, len(self.DCRGraph.InitialIncluded))
        self.assertEqual(2, len(deepcopy_test.Included))
        self.assertEqual(2, len(deepcopy_test.Executed))
        self.assertEqual(4, len(self.InitialMarking.Included))
        self.assertEqual(0, len(self.InitialMarking.Executed))

        self.assertEqual(deepcopy_test.PendingResponse[0],
                         self.InitialMarking.PendingResponse[0])

    def test_exclude_relation(self):
        copied_marking = Marking.get_initial_marking()
        start_node = self.DCRGraph.get_node('Activity0')
        end_node = self.DCRGraph.get_node('Activity1')
        exclude_connection = DCRConnection.create_connection(start_node, end_node, ConnectionTypes.exclude)

        self.assertIsInstance(exclude_connection, Exclude)

        exclude_connection.perform_transition(copied_marking)

        self.assertTrue(end_node not in copied_marking.Included)
        self.assertTrue(end_node in self.InitialMarking.Included)

    def test_include_relation(self):
        start_node = self.DCRGraph.get_node('Activity0')
        end_node = self.DCRGraph.get_node('Activity1')
        include_connection = DCRConnection.create_connection(start_node, end_node, ConnectionTypes.include)
        self.assertIsInstance(include_connection, Include)
        self.DCRGraph.add_connection(include_connection)

        self.InitialMarking.Included.remove(end_node)
        self.assertTrue(end_node not in self.InitialMarking.Included)

        include_connection.perform_transition(self.InitialMarking)
        self.assertTrue(end_node in self.InitialMarking.Included)

    def test_node_is_blocked_milestone(self):
        self.InitialMarking.get_initial_marking()
        start_node = self.DCRGraph.get_node('Activity0')
        end_node = self.DCRGraph.get_node('Activity1')
        trace_data = MagicMock()
        attributes = MagicMock()
        self.assertTrue(end_node.IsMilestoneTarget)
        self.assertTrue(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))

        self.InitialMarking.Included.remove(start_node)
        self.assertFalse(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))

        self.InitialMarking.Included.append(start_node)
        self.assertTrue(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))

        self.InitialMarking.PendingResponse.remove(start_node)
        self.assertFalse(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))

    def test_node_is_blocked_condition(self):
        self.InitialMarking.get_initial_marking()
        start_node = self.DCRGraph.get_node('Activity0')
        end_node = self.DCRGraph.get_node('Activity1')
        trace_data = MagicMock()
        attributes = MagicMock()

        condition_connection = DCRConnection.create_connection(start_node, end_node, ConnectionTypes.condition)  #
        self.DCRGraph.add_connection(condition_connection)
        self.DCRGraph.set_condition_targets()

        self.assertTrue(end_node.IsConditionTarget)
        self.assertTrue(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))

        self.InitialMarking.Included.remove(start_node)

        self.assertFalse(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))

        self.InitialMarking.Included.append(start_node)
        self.assertTrue(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))

        self.InitialMarking.Executed.append(start_node)
        self.assertTrue(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))
        self.InitialMarking.PendingResponse.remove(start_node)
        self.assertFalse(self.InitialMarking.node_is_blocked(end_node, trace_data, attributes))


if __name__ == '__main__':
    unittest.main()
