# This module uses NumPy style docstrings: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
r"""This example shows a game of PingPong using protocols in NetSquid.

The PingPong game is played with two players, which we call Ping and Pong.
The game starts when the Ping entity sends a qubit to the Pong entity.
When Pong receives it, it measures the qubit in the Hadamard (X) basis,
and then sends the qubit back to the Ping entity.
On receiving the qubit, it is the Ping entity's turn to measure it in the
standard (Z) basis, and to send the qubit to the Pong entity again, etc.

The protocol used is a :py:obj:`~netsquid_pingpong.protocols.PingPongProtocol`.
We can run two of these protocols on the nodes of our Ping and Pong entity.
We connect them with a direct connection, assign them their protocol and start the simulation.
The components in the network are represented in the following figure.

.. aafig::
    :scale: 100
    :textual:
    :align: center

    +--------------------+   +-----------------------------------------+   +--------------------+
    |                    |   |            "DirectConnection"           |   |                    |
    |                    |   |                                         |   |                    |
    |                    |   |        +----------------------+         |   |                    |
    |                    |   |         \                      \        |   |                    |
    |                    |   |    +-->-O+  "QuantumChannel"   O-->-    |   |                    |
    |                    |   |   /     /                      /    \   |   |                    |
    |       "Node"       |   |  /     +----------------------+      \  |   |       "Node"       |
    |       "Ping"       O---O-+                                     +-O---O       "Pong"       |
    |                    |   |  \       +----------------------+    /  |   |                    |
    |                    |   |   \     /                      /    /   |   |                    |
    |                    |   |    +-<--O  "QuantumChannel"   +O--<-    |   |                    |
    |                    |   |         \                      \        |   |                    |
    |                    |   |          +----------------------+       |   |                    |
    |                    |   |                                         |   |                    |
    +--------------------+   +-----------------------------------------+   +--------------------+

The code to run the example is given below.

"""

import netsquid as ns
from netsquid_pingpong.protocols import PingPongProtocol
from netsquid_pingpong.models import PingPongDelayModel
from netsquid.nodes import Node, DirectConnection
from netsquid.components import QuantumChannel


def main():
    # Initialise the simulation.
    ns.sim_reset()
    distance = 2.74 / 1000  # default unit of length in channels is km
    delay_model = PingPongDelayModel()

    # Set-up the network.
    node_ping = Node("Ping", port_names=["port_to_channel"])
    node_pong = Node("Pong", port_names=["port_to_channel"])
    connection = DirectConnection("Connection",
                                  QuantumChannel(name="qchannel[ping to pong]",
                                                 length=distance,
                                                 models={"delay_model": delay_model}),
                                  QuantumChannel(name="qchannel[pong to ping]",
                                                 length=distance,
                                                 models={"delay_model": delay_model}))
    node_ping.connect_to(remote_node=node_pong, connection=connection,
                         local_port_name="qubitIO", remote_port_name="qubitIO")

    # Assign protocols to the nodes.
    qubits = ns.qubits.create_qubits(1)
    ping_protocol = PingPongProtocol(node_ping, observable=ns.Z, qubit=qubits[0])
    pong_protocol = PingPongProtocol(node_pong, observable=ns.X)

    # Start the protocols and the simulation.
    print("Start the PingPong simulation:\n")
    ping_protocol.start()
    pong_protocol.start()
    stats = ns.sim_run(91)
    print(stats)


if __name__ == "__main__":
    main()
