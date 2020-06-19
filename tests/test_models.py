# This module uses NumPy style docstrings: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
"""Unit tests for the models module.

This file will be discovered by ``python setup.py test``.

"""
import unittest
import numpy as np
import netsquid.util.simtools as simtools
from netsquid_pingpong.models import PingPongDelayModel


class TestPingPongDelayModel(unittest.TestCase):
    """Unit tests for PingPong Delay Model.

    """

    def setUp(self):
        simtools.set_random_state(rng=np.random.RandomState(0))  # reset RNG

    def test_init(self):
        """Verify the initialisation of a PingPongDelayModel."""
        speed_of_light_fraction = .1
        standard_deviation = 0.2
        model = PingPongDelayModel(speed_of_light_fraction, standard_deviation)
        self.assertEqual(model.properties['speed'], speed_of_light_fraction * 3e5)
        self.assertEqual(model.properties['std'], standard_deviation)

    def test_PingPongDelayModel(self):
        """Test delay model with different parameters."""
        # No standard deviation
        length = 1
        model = PingPongDelayModel(speed_of_light_fraction=1, standard_deviation=0)
        self.assertAlmostEqual(model(length=length), 1e9 / 3e5)
        # Default values with fixed rng
        model = PingPongDelayModel()
        self.assertAlmostEqual(model(length=length), 6535.8973448815395)
        # Length most be provided to the call
        with self.assertRaises(KeyError):
            model()


if __name__ == "__main__":
    unittest.main()
