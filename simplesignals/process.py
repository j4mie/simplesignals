import sys
import logging
from simplesignals import signals

logger = logging.getLogger('simplesignals.process')


class WorkerProcessBase(object):

    """
    Simple base class for worker processes that implement a main
    loop, doing some work repeatedly. This class provides a way to
    gracefully shut down when int, quit or term signals are received.
    """

    def __init__(self):
        self.alive = True
        self.set_process_title()
        self.init_signals()

    def set_process_title(self):
        logger.debug("Attempting to set process title")
        try:
            from setproctitle import setproctitle
        except ImportError:
            logger.debug("Failed to import setproctitle, skipping")
            return

        title = getattr(self, 'process_title',
                        self.__class__.__name__.lower())

        logger.debug("Setting process title to %s", title)
        setproctitle(title)

    def init_signals(self):
        logger.debug("Initializing signal handlers")
        signals.int(allow_interrupt=False)(self.shutdown)
        signals.quit(allow_interrupt=False)(self.shutdown)
        signals.term(allow_interrupt=False)(self.shutdown)

    def shutdown(self):
        logger.debug("Shutting down process")
        self.alive = False

    def run(self):
        logger.debug("Starting process")

        self.startup()

        while self.alive:
            self.do_work()

        self.cleanup()
        logger.debug("Exiting process")
        sys.exit(0)

    def do_work(self):
        raise NotImplementedError()

    def startup(self):
        pass

    def cleanup(self):
        pass
