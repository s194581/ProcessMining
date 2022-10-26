# coding=utf-8
"""Used to check the parsing of a DCR graph"""
import os
import unittest

import graph


class FixedXmlGraphTestCase(unittest.TestCase):

    def setUp(self):
        self.DCRGraph = graph.DCRGraph(os.path.join(os.path.dirname(__file__), 'test_resources/FixedXmlTest.xml'))

    def test_len_activities(self):
        self.assertEqual(len(self.DCRGraph.Nodes), 4)

    def test_len_connections(self):
        self.assertEqual(len(self.DCRGraph.Connections), 4)

    def test_len_expressions(self):
        self.assertEqual(len(self.DCRGraph.Expressions), 2)

    def test_get_expr(self):
        expression = self.DCRGraph.get_expression('Activity1-path-Activity2--response')
        self.assertEqual(expression.expression_left, 'costs')
        self.assertEqual(expression.expression_right, 100)
        self.assertEqual(expression.expression_middle, '>')

    def test_get_node_by_name(self):
        activity0 = self.DCRGraph.get_node("Activity0")
        activity01 = self.DCRGraph.get_node_by_name(activity0.ActivityName)

        self.assertIs(activity0, activity01)

    def test_get_node(self):
        activity0 = self.DCRGraph.get_node("Activity0")
        activity1 = self.DCRGraph.get_node("Activity1")
        activity2 = self.DCRGraph.get_node("Activity2")
        activity3 = self.DCRGraph.get_node("Activity3")

        self.assertIsNotNone(activity0)
        self.assertIsNotNone(activity1)
        self.assertIsNotNone(activity2)
        self.assertIsNotNone(activity3)

        self.assertEqual(activity0.Roles[0], 'employee')
        self.assertEqual(activity0.ActivityName, 'Receive PO')

        self.assertEqual(activity1.Roles[0], 'employee')
        self.assertEqual(activity1.ActivityName, 'Setup Order')

        self.assertEqual(activity2.Roles[0], 'manager')
        self.assertEqual(activity2.ActivityName, 'Review')

        self.assertEqual(activity3.Roles, [])
        self.assertEqual(activity3.ActivityName, 'Place Order')


class MileStoneTestCase(unittest.TestCase):

    def setUp(self):
        self.DCRGraph = graph.DCRGraph(os.path.join(os.path.dirname(__file__),
                                                    'test_resources/TestCase_Milestone_Condition.xml'))

    def test_activities(self):
        activity0 = self.DCRGraph.get_node("Activity0")
        activity1 = self.DCRGraph.get_node("Activity1")
        activity2 = self.DCRGraph.get_node("Activity2")
        activity3 = self.DCRGraph.get_node("Activity3")

        self.assertIsNotNone(activity0)
        self.assertIsNotNone(activity1)
        self.assertIsNotNone(activity2)
        self.assertIsNotNone(activity3)

        self.assertEqual(activity0.Roles[0], 'employee')
        self.assertEqual(activity0.ActivityName, 'Receive PO')

        self.assertEqual(activity1.Roles[0], 'employee')
        self.assertEqual(activity1.ActivityName, 'Setup Order')

        self.assertEqual(activity2.Roles[0], 'manager')
        self.assertEqual(activity2.ActivityName, 'Review')

        self.assertEqual(activity3.Roles[0], 'employee')
        self.assertEqual(activity3.ActivityName, 'Place Order')

    def test_get_milestone_targets(self):
        self.assertEqual(len(self.DCRGraph.MilestoneTargets), 1)
        milestone_target = self.DCRGraph.MilestoneTargets[0]
        self.assertEqual(milestone_target.ActivityId, 'Activity1')
        self.assertEqual(milestone_target.Roles, ['employee'])
        self.assertEqual(milestone_target.ActivityName, 'Setup Order')

    def test_get_condition_targets(self):
        self.assertEqual(1, len(self.DCRGraph.ConditionTargets))
        condition_target = self.DCRGraph.ConditionTargets[0]
        self.assertEqual('Activity3', condition_target.ActivityId)
        self.assertEqual(['employee'], condition_target.Roles)
        self.assertEqual('Place Order', condition_target.ActivityName)


if __name__ == '__main__':
    unittest.main()
