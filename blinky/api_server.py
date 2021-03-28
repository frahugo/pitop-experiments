#
# A simple Python server and an Elixir client sending to it
# Python server will reply with its own Pid, so then you know the Pid and can
# send to it directly (second send call).
#
# Run `make example10a` to run Python node
# Run `make example10b` to run Elixir client which will perform the call
#

import logging
import multiprocessing

from term import Atom
from pyrlang.gen.server import GenServer
from pyrlang.gen.decorators import call, cast, info
from pyrlang import Node

# In elixir:
# n = {:api_server, :"pitop@pi-top.local"}
# pid = GenServer.call(n, "hello")
# GenServer.call(pid, "start_blink")
# GenServer.call(pid, "stop_blink")

class ApiServerProcess(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        node = Node(node_name="pitop@pi-top.local", cookie="ilfautbienquedesbonslegosoientvendussurrlinternet")
        ApiServer(node, self.queue)
        node.run()

class ApiServer(GenServer):
    def __init__(self, node, queue) -> None:
        super().__init__()
        node.register_name(self, Atom('api_server'))
        self.queue = queue

    @call(1, lambda msg: msg == b'hello')
    def hello(self, msg):
        return self.pid_

    @call(2, lambda msg: msg == b'welcome')
    def welcome(self, msg):
        self.queue.put('welcome')
        return b'Display welcome message...'

    @call(3, lambda msg: msg == b'start_blink')
    def start_blink(self, msg):
        self.queue.put('start_blink')
        return b'Blinking...'

    @call(4, lambda msg: msg == b'stop_blink')
    def stop_blink(self, msg):
        self.queue.put('stop_blink')
        return b'Stop blinking...'
