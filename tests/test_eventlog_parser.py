import os
import unittest

import eventlog_parser


class Xes_parser_tests(unittest.TestCase):

    def test_parse_xes(self):
        event_log = eventlog_parser.get_event_log(os.path.join(os.path.dirname(__file__),
                                                               './test_resources/event_log.xes'))
        self.assertTrue(len(event_log.Traces) == 132)
        for trace in event_log.Traces:
            self.assertIsNotNone(trace.Events)
            for event in trace.Events:
                self.assertIsNotNone(event.EventName)
                self.assertIsNotNone(event.Timestamp)
                self.assertIsNotNone(event.Attributes)
                self.assertIsNotNone(event.Role)


if __name__ == '__main__':
    unittest.main()
