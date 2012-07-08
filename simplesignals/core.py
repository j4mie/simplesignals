import signal
import logging

logger = logging.getLogger('simplesignals.core')


class Signal(object):

    """
    Represents a signal. Can be used to convert between signal name
    and signal number, and compare with other Signals. Also used as
    a decorator to register functions as signal handlers.
    """

    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __repr__(self):
        return 'Signal(number=%s, name=%s)' % (self.number, self.name)

    def __int__(self):
        return self.number

    def __str__(self):
        return self.name

    def __eq__(self, other):
        """
        Compare this signal against another signal, either
        a Signal instance, integer number, or string name.
        """

        if isinstance(other, Signal):
            return int(self) == int(other)

        if isinstance(other, int):
            return int(self) == other

        if isinstance(other, str):
            return str(self) == other

    def __call__(self, *args, **kwargs):

        allow_interrupt = kwargs.get('allow_interrupt', True)
        takes_signal = kwargs.get('takes_signal', False)
        takes_frame = kwargs.get('takes_frame', False)

        def decorator(func):
            logger.debug("Attaching handler for %s", self)
            handler = SignalHandler(func, takes_frame=takes_frame,
                                    takes_signal=takes_signal)
            signal.signal(int(self), handler)

            if hasattr(signal, 'siginterrupt'):  # python 2.6
                signal.siginterrupt(int(self), allow_interrupt)

            return func

        # Make sure the decorator works with or without arguments
        if len(args) == 1 and callable(args[0]):
            return decorator(args[0])
        return decorator

    def get_handler(self):
        """
        Return the handler function attached to this signal
        """
        return signal.getsignal(int(self))


class SignalHandler(object):

    """
    Wraps a signal handler function and ensures it gets called
    with the correct arguments, logs calls, etc
    """

    def __init__(self, handler_func, takes_signal=False, takes_frame=False):
        self.handler_func = handler_func
        self.takes_signal = takes_signal
        self.takes_frame = takes_frame

    def __call__(self, signal_number, frame):
        signal = signals[signal_number]
        logger.debug("Handling %s", signal)

        handler_args = []
        if self.takes_signal:
            handler_args.append(signal)
        if self.takes_frame:
            handler_args.append(frame)

        return self.handler_func(*handler_args)


class SignalNamespace(object):

    """
    A flexible way of converting between signal names and
    numbers. Supports attribute access for name lookup, as well as
    index lookup by name or number. Each of these methods returns a
    Signal instance, which can be cast to a string or an int to convert
    to the desired representation.
    """

    def __init__(self):
        self.signals = {}

        # Populate with constants found in the built-in signal module
        for name in dir(signal):
            if name[:3] == 'SIG' and name[3] != '_':
                number = getattr(signal, name)
                self.add_signal(number, name[3:].lower())

    def add_signal(self, number, name):
        signal = Signal(number, name)
        self.signals[number] = signal
        self.signals[name] = signal
        setattr(self, name, signal)

    def __getitem__(self, name):
        return self.signals[name]


signals = SignalNamespace()
