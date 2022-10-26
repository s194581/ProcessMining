# coding=utf-8
"""
Used to check Connection functionality
"""
import unittest

from expr import Expression, Comparators


class TestConnectionsMethods(unittest.TestCase):
    def setUp(self):
        self.expression = Expression()

    def test_convert_right_side_float(self):
        """
        Tests if the right side can be correctly evaluated
        :return:
        """
        expression_str = 'costs!=4.3'
        self.expression.split_singular_expression(expression_str)
        self.expression.try_convert_expression_right()
        self.assertTrue(type(self.expression.expression_right) is float)
        self.assertEqual(self.expression.expression_right, 4.3)
        self.assertEqual(self.expression.expression_left, 'costs')
        self.assertEqual(self.expression.expression_middle, '!=')

    def test_convert_right_side_bool(self):
        """
        Tests if the right side can be correctly evaluated
        :return:
        """
        expression_str = 'Walter=True'
        self.expression.split_singular_expression(expression_str)
        self.expression.try_convert_expression_right()
        self.assertTrue(type(self.expression.expression_right) is bool)
        self.assertEqual(self.expression.expression_right, True)
        self.assertEqual(self.expression.expression_left, 'Walter')
        self.assertEqual(self.expression.expression_middle, '=')

    def test_convert_right_side_int(self):
        """
        Tests if the right side can be correctly evaluated
        :return:
        """
        expression_str = 'Int=12'
        self.expression.split_singular_expression(expression_str)
        self.expression.try_convert_expression_right()
        self.assertTrue(type(self.expression.expression_right) is int)
        self.assertEqual(self.expression.expression_right, 12)
        self.assertEqual(self.expression.expression_left, 'Int')
        self.assertEqual(self.expression.expression_middle, '=')

    def test_convert_right_side_str(self):
        """
        Tests if the right side can be correctly evaluated
        :return:
        """
        expression_str = 'Driver=Driver'
        self.expression.split_singular_expression(expression_str)
        self.expression.try_convert_expression_right()
        self.assertTrue(type(self.expression.expression_right) is str)
        self.assertEqual(self.expression.expression_right, 'Driver')
        self.assertEqual(self.expression.expression_left, 'Driver')
        self.assertEqual(self.expression.expression_middle, '=')

    def test_split_expression_greater_simple(self):
        """
        Uses the expression costs>3
        :return:
        """
        expression_str = 'costs>3'
        self.expression.split_singular_expression(expression_str)
        self.assertEqual(self.expression.expression_left, 'costs')
        self.assertEqual(self.expression.expression_middle, '>')
        self.assertEqual(self.expression.expression_right, '3')

    def test_split_expression_smaller_simple(self):
        """
        Uses the expression "loss<55"
        :return:
        """
        expression_str = 'loss<55'
        self.expression.split_singular_expression(expression_str)
        self.assertEqual(self.expression.expression_left, 'loss')
        self.assertEqual(self.expression.expression_middle, '<')
        self.assertEqual(self.expression.expression_right, '55')

    def test_split_expression_equals_simple(self):
        """

        :return:
        """
        expression_str = 'state=Cool'
        self.expression.split_singular_expression(expression_str)
        self.assertEqual(self.expression.expression_left, 'state')
        self.assertEqual(self.expression.expression_middle, '=')
        self.assertEqual(self.expression.expression_right, 'Cool')

    def test_split_expression_smaller_equal_simple(self):
        """
        Uses the expression "loss<55"
        :return:
        """
        expression_str = 'costs<=55'
        self.expression.split_singular_expression(expression_str)
        self.assertEqual(self.expression.expression_left, 'costs')
        self.assertEqual(self.expression.expression_middle, '<=')
        self.assertEqual(self.expression.expression_right, '55')

    def test_split_expression_whitespace(self):
        """

        :return:
        """
        expression_str = ' costs <= 55 '
        self.expression.split_singular_expression(expression_str)
        self.assertEqual(self.expression.expression_left, 'costs')
        self.assertEqual(self.expression.expression_middle, '<=')
        self.assertEqual(self.expression.expression_right, '55')

    def test_split_isNot_whitespaceInComparison(self):
        """

        :return:
        """
        expression_str = ' costs = ! 55 '
        self.expression.split_singular_expression(expression_str)
        self.assertEqual(self.expression.expression_left, 'costs')
        self.assertEqual(self.expression.expression_middle, '=!')
        self.assertEqual(self.expression.expression_right, '55')

    def test_convert_comparator_gte0(self):
        """

        :return:
        """
        expression_str = 'costs>=xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '>=')
        self.assertEqual(self.expression.expression_comparator, Comparators.gte)

    def test_convert_comparator_gte1(self):
        """

        :return:
        """
        expression_str = 'costs=>xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '=>')
        self.assertEqual(self.expression.expression_comparator, Comparators.gte)

    def test_convert_comparator_lte0(self):
        """

        :return:
        """
        expression_str = 'costs=<xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '=<')
        self.assertEqual(self.expression.expression_comparator, Comparators.lte)

    def test_convert_comparator_lte1(self):
        """

        :return:
        """
        expression_str = 'costs<=xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '<=')
        self.assertEqual(self.expression.expression_comparator, Comparators.lte)

    def test_convert_comparator_lt(self):
        """

        :return:
        """
        expression_str = 'costs<xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '<')
        self.assertEqual(self.expression.expression_comparator, Comparators.lt)

    def test_convert_comparator_gt(self):
        """

        :return:
        """
        expression_str = 'costs>xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '>')
        self.assertEqual(self.expression.expression_comparator, Comparators.gt)

    def test_convert_comparator_eq0(self):
        """

        :return:
        """
        expression_str = 'costs=xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '=')
        self.assertEqual(self.expression.expression_comparator, Comparators.eq)

    def test_convert_comparator_eq1(self):
        """

        :return:
        """
        expression_str = 'costs==xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '==')
        self.assertEqual(self.expression.expression_comparator, Comparators.eq)

    def test_convert_comparator_neq0(self):
        """

        :return:
        """
        expression_str = 'costs!xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '!')
        self.assertEqual(self.expression.expression_comparator, Comparators.neq)

    def test_convert_comparator_neq1(self):
        """

        :return:
        """
        expression_str = 'costs!!xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '!!')
        self.assertEqual(self.expression.expression_comparator, Comparators.neq)

    def test_convert_comparator_neq2(self):
        """

        :return:
        """
        expression_str = 'costs!=xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '!=')
        self.assertEqual(self.expression.expression_comparator, Comparators.neq)

    def test_convert_comparator_neq3(self):
        """

        :return:
        """
        expression_str = 'costs=!xxx'
        self.expression.split_singular_expression(expression_str)
        self.expression.convert_comparator()
        self.assertEqual(self.expression.expression_middle, '=!')
        self.assertEqual(self.expression.expression_comparator, Comparators.neq)


if __name__ == '__main__':
    unittest.main()
