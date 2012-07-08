# simplesignals

**Unix signal handlers and worker processes, simplified.**

**Author:** Jamie Matthews. [Follow me on Twitter](http://twitter.com/j4mie).

## Documentation

This project provides a layer on top of the built-in [signal](http://docs.python.org/library/signal.html) module. It allows you to easily register functions as handlers for [Unix signals](http://en.wikipedia.org/wiki/Unix_signal). It also provides a lightweight base class for implementing basic Unix worker processes.

### Signal handlers

The library provides a set of function decorators, one for each signal type, which you can use to declare a function as a signal handler. For example, to connect a handler function to the `SIGINT` signal:

    from simplesignals import signals

    @signals.int
    def handler():
        print "Bye then!"
        exit()

If you want to use the same function to handle multiple signals, you can stack the decorators and ask that the signal be passed on to your handler function:

    from simplesignals import signals

    @signals.int(takes_signal=True)
    @signals.term(takes_signal=True)
    @signals.quit(takes_signal=True)
    def handler(signal):
        if signal == signals.int:
            print "Got int!"
        # ... etc
        exit()

If you need the execution frame that would be handed to your function by the `signal` module, you can ask for that too:

    from simplesignals import signals

    @signals.quit(takes_frame=True)
    def handler(frame):
        # do something with frame
        exit()

System call interrupt behaviour can be controlled with the `allow_interrupt` flag. See [the `signal` module docs](http://docs.python.org/library/signal.html#signal.siginterrupt) for details.

### Worker processes

One of the primary uses of Unix signals is to implement well-behaved worker processes. Process management tools such as [Circus](http://circus.io) use signals to communicate with your processes. If you can handle signals correctly, you can take the opportunity to gracefully shut down your process and avoid half-finished jobs, etc.

An extremely simple base class is provided which currently provides the following:

* A main loop that allows your process to perform its work.
* Graceful shutdown on `SIGINT`, `SIGTERM` and `SIGQUIT`.
* Sets the title of the process if [setproctitle](http://code.google.com/p/py-setproctitle/) is installed.

A simple example:

    from simplesignals.process import WorkerProcessBase

    class MyWorker(WorkerProcessBase):

         process_title = "my-worker"

         def do_work(self):
             # this method is called repeatedly, do your work here
             # eg. get item from a queue and process it
             self.do_some_really_super_hard_work()

    if __name__ == "__main__":
        worker = Worker()
        worker.run()

Please take a look at the source code to understand exactly what functionality `WorkerProcessBase` provides.


## Changelog

#### 0.2.0

* Disallow interrupts in WorkerProcessBase signal handlers

#### 0.1.0

* Initial release.

## Installation

You can install simplesignals from PyPI:

    pip install simplesignals

## Development

To contribute: fork the repository, make your changes, add some tests, commit,
push to a feature branch, and open a pull request.

### How to run the tests

`pip install -r requirements.txt` then `python tests.py`

## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
