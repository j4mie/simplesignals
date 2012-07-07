import mock
import unittest
from simplesignals.core import Signal, SignalHandler, SignalNamespace


class SignalTestCase(unittest.TestCase):

    def setUp(self):
        self.signal = Signal(2, 'int')

    def test_convert_to_number(self):
        self.assertEqual(self.signal, 2)

    def test_convert_to_string(self):
        self.assertEqual(self.signal, 'int')

    @mock.patch('signal.signal')
    def test_attach_handler(self, mock_signal):

        def side_effect(signal_number, handler):
            self.assertEqual(signal_number, self.signal)
            self.assertIsInstance(handler, SignalHandler)
            self.assertEqual(handler(2, None), "result")
        mock_signal.side_effect = side_effect

        @self.signal
        def handler():
            return "result"

    @mock.patch('signal.signal')
    def test_takes_frame(self, mock_signal):

        def side_effect(signal_number, handler):
            self.assertTrue(handler.takes_frame)
        mock_signal.side_effect = side_effect

        @self.signal(takes_frame=True)
        def handler(frame):
            pass

    @mock.patch('signal.signal')
    def test_takes_signal(self, mock_signal):

        def side_effect(signal_number, handler):
            self.assertTrue(handler.takes_signal)
        mock_signal.side_effect = side_effect

        @self.signal(takes_signal=True)
        def handler(frame):
            pass

    @mock.patch('signal.siginterrupt')
    def test_allow_interrupt(self, mock_siginterrupt):

        @self.signal(allow_interrupt=False)
        def handler():
            pass

        mock_siginterrupt.assert_called_with(int(self.signal), False)


class SignalHandlerTestCase(unittest.TestCase):

    def test_handler_called(self):

        def handler():
            return "result"

        wrapped_handler = SignalHandler(handler)
        result = wrapped_handler(2, None)
        self.assertEqual(result, "result")

    def test_takes_frame(self):

        def handler(frame):
            return frame

        wrapped_handler = SignalHandler(handler, takes_frame=True)
        result = wrapped_handler(2, "fakeframe")
        self.assertEqual(result, "fakeframe")


class SignalNamespaceTestCase(unittest.TestCase):

    def test_namespace_lookup(self):
        signals = SignalNamespace()
        self.assertIsInstance(signals.int, Signal)
        self.assertEqual(signals.int, 2)
        self.assertEqual(signals['int'], 2)
        self.assertEqual(signals[2], 'int')


if __name__ == "__main__":
    unittest.main()
