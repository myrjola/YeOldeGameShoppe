from django.test import TestCase


class FailingTestCase(TestCase):
    def this_will_fail(self):
        """This test will fail"""
        self.assertEqual(True, False)
