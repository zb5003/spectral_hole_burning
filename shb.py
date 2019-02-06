from physicalparameters import *
from ..diff_eq import firstorderconsthomo as foch
import scipy as sp


class SHB:

    def __init__(self, beams, atom):
        """

        :param beams: List of instances of class beam.
        :param atom:
        """
        self.beams = beams
        self.atom = atom

        self.atoms = self._generate_atoms()
        self._permissions()
        self.operators = self._generate_evolution_operators()

    def _generate_atoms(self):
        """
        Generate that atom class instances with proper detunings.
        :return:
        """
        atoms = []
        for beam in self.beams:
            atoms.append(Atom(self.atom.decay_rates,
                              self.atom.dipole_moments,
                              self.atom.lower_splittings,
                              self.atom.upper_splittings,
                              detuning=beam.detuning))
        return atoms

    def _permissions(self):
        """

        :return:
        """
        for atom in self.atoms:
            for cls in atom.classes:
                for transition in atom.classes[cls][1]:
                    for beam in self.beams:
                        if transition[1] == beam.detuning:
                            transition[2] = beam.label
        return None

    def _generate_evolution_operators(self):
        """

        :return:
        """
        operators = []
        for atom in self.atoms:
            for cls in atom.classes:
                operator = sp.zeros((atom.n_lower + atom.n_upper, atom.n_lower + atom.n_upper))
                for transition in atom.classes[cls][1]:
                    for beam in self.beams:
                        if transition[2] == beam.label:
                            r = self.pump_rate(beam.detuning)
                            operator[transition[0][0] - 1, transition[0][1] - 1] = -r
                            operator[transition[0][1] - 1, transition[0][0] - 1] = r
                operators.append(operator)
        return operators

    def pump_rate(self, detuning):
        """

        :param detuning:
        :return:
        """
        return NotImplementedError
