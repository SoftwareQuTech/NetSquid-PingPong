# This moduls uses NumPy style docstrings: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
"""Unit tests for the protocols module.

This file will be discovered by ``python setup.py test``.

"""
import unittest
import sys
import io
import netsquid as ns
from netsquid.nodes import Node
from netsquid_pingpong.protocols import PingPongProtocol


class TestPingPongProtocol(unittest.TestCase):
    """Unit tests for PingPong Protocol.

    """
    def _get_printed_output(self, function):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        function()
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def setUp(self):
        ns.sim_reset()
        # self.helper = pydynaa.Entity()  # helper entity
        self.node = Node(name="TestNode", port_names=["qubitIO"], ID=0)
        ns.set_random_state(seed=42)

    def test_constructor(self):
        qubits = ns.qubits.create_qubits(1)
        # Test initialisation without and with qubit
        protocol_test_1 = PingPongProtocol(self.node, ns.Z)
        self.assertEqual(protocol_test_1.observable, ns.Z)
        self.assertIsNone(protocol_test_1.qubit)
        protocol_test_2 = PingPongProtocol(self.node, ns.Z, qubit=qubits[0])
        self.assertEqual(protocol_test_2.qubit, qubits[0])

    def test_running(self):
        qubits = ns.qubits.create_qubits(1)
        p = PingPongProtocol(self.node, observable=ns.Z, qubit=qubits[0])
        p.start()
        self.assertTrue(p.is_running)
        self.assertEqual(len(self.node.ports["qubitIO"].output_queue), 1)
        ns.sim_run(3)
        self.assertTrue(p.is_running)
        self.assertEqual(len(self.node.ports["qubitIO"].output_queue), 1)
        self.node.ports["qubitIO"].tx_input(qubits[0])
        output = self._get_printed_output(ns.sim_run)
        expected_output = "  3.0: TestNode measured |0> with probability 1.00\n"
        self.assertEqual(output, expected_output)

        # Running without qubit should result in no output queue
        ns.sim_reset()
        node2 = Node(name="TestNode2", port_names=["qubitIO"])
        p2 = PingPongProtocol(node2, observable=ns.X)
        p2.start()
        self.assertTrue(p2.is_running)
        self.assertEqual(len(node2.ports["qubitIO"].output_queue), 0)

        qubits = ns.qubits.create_qubits(1)
        node2.ports["qubitIO"].tx_input(qubits[0])
        output = self._get_printed_output(ns.sim_run)
        expected_output = "  0.0: TestNode2 measured |-> with probability 0.50\n"
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
