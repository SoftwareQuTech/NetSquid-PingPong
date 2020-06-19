# This module uses NumPy style docstrings: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
"""Module containing a PingPong protocol.

The protocol in this module is written in a way it can be used on both players of a PingPong game.
Each player will have their own protocol running on their own node.
In short the protocol measures an arriving qubit, prints the result and sends the qubit back.

An implementation of a game of PingPong can be found in the examples directory.

"""
import netsquid as ns
from netsquid.protocols import NodeProtocol

__all__ = [
    "PingPongProtocol"
]


class PingPongProtocol(NodeProtocol):
    """Protocol that runs on one node which can be used for a game of PingPong.

    Parameters
    ----------
    node : :class:`~netsquid.nodes.node.Node` or None
        Node this protocol runs on. If None, a node should be set later before starting
        this protocol.
    observable : :obj:`~netsquid.qubits.operators.Operator`
        Hermitian operator to measure qubit with.
    qubit : :obj:`netsquid.qubits.Qubit`, optional
        Qubit to play PingPong with. Only one of the players needs to start with a qubit. Default None.

    """
    def __init__(self, node, observable, qubit=None):
        super().__init__(node)
        self.observable = observable
        self.qubit = qubit
        # Define matching pair of strings for pretty printing of basis states:
        self.basis = ["|0>", "|1>"] if observable == ns.Z else ["|+>", "|->"]

    def run(self):
        """Generator or function that runs the PingPong protocol.

        Starting the protocol will execute this function.
        As a generator it will run up to the first yield statement.
        The generator will only continue when the expression yielded on has been triggered.

        When a qubit is provided to the protocol, it will put it on its IO port to start the game.
        It will wait until a qubit arrives at its IO port.
        This qubit is measured, the result printed and the qubit is send to the IO port again.

        """
        if self.qubit is not None:
            # Send (TX) qubit to the other node via port's output:
            self.node.ports["qubitIO"].tx_output(self.qubit)
        while True:
            # Wait (yield) until input has arrived on our port:
            yield self.await_port_input(self.node.ports["qubitIO"])
            # Receive (RX) qubit on the port's input:
            message = self.node.ports["qubitIO"].rx_input()
            qubit = message.items[0]
            meas, prob = ns.qubits.measure(qubit, observable=self.observable)
            print(f"{ns.sim_time():5.1f}: {self.node.name} measured "
                  f"{self.basis[meas]} with probability {prob:.2f}")
            # Send (TX) qubit to the other node via connection:
            self.node.ports["qubitIO"].tx_output(qubit)
