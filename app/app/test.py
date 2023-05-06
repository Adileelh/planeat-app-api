"""
Sample test
"""

from django.test import SimpleTestCase

from app import calc


class CalculateTest(SimpleTestCase):
    """
    Sample test
    """

    def test_add_numbers(self):
        """
        Test the calc function
        """

        self.assertEqual(calc.add(2, 2), 4)

    def test_subtract(self):
        """
        Subtract two numbers
        """

        self.assertEqual(calc.subtract(2, 2), 0)
