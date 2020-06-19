# This module uses NumPy style docstrings: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
"""Module containing custom models for the PingPong game.

"""
from netsquid.components.models import DelayModel

__all__ = [
    "PingPongDelayModel"
]


class PingPongDelayModel(DelayModel):
    """Delay model which can be used for a game of PingPong at (a fraction of) the speed of light (300,000 km/s).

    Parameters
    ----------
    speed_of_light_fraction : float, optional
        Fraction of the speed of light at which the qubits will travel. Default 0.5.
    standard_deviation : float, optional
        Standard deviation of the speed at which the qubits will travel. Default 0.05.

    """
    def __init__(self, speed_of_light_fraction=0.5, standard_deviation=0.05):
        super().__init__()
        self.properties["speed"] = speed_of_light_fraction * 3e5
        self.properties["std"] = standard_deviation
        self.required_properties = ['length']  # in km

    def generate_delay(self, **kwargs):
        """Generate a timing delay.

        Returns
        -------
        float
            Delay [ns].

        Raises
        ------
        KeyError
            If the ``QuantumChannel`` does not have a ``length`` attribute or this
            function is called directly without a ``length`` argument.

        """
        avg_speed = self.properties["speed"]
        std = self.properties["std"]
        # The 'rng' property contains a random number generator
        # We can use that to generate a random speed
        speed = self.properties["rng"].normal(avg_speed, avg_speed * std)
        delay = 1e9 * kwargs['length'] / speed  # in nanoseconds
        return delay
